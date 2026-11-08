from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import sys
import os
import json
import requests
from uuid import uuid4

from database import get_db
from models import User, Conversation, ChatMessage, MessageRole, Video
from schemas import ChatRequest, ChatResponse, SourceCitation, ConversationResponse
from security import decode_token
from embeddings import create_embedding
from qdrant_helper import search
from config import OLLAMA_URL

app = FastAPI(title="Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_user(token: str, db: Session):
    """Helper to get current user from token"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

def generate_response(prompt: str) -> str:
    """Generate response using DeepSeek via Ollama"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "deepseek-r1:1.5b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print(f"Error generating response: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate response"
        )

def format_timestamp(seconds: float) -> str:
    """Format seconds to MM:SS"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "chat-api"}

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)

    # Get or create conversation
    if request.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == request.conversation_id,
            Conversation.user_id == user.id
        ).first()
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        # Create new conversation
        conversation = Conversation(
            user_id=user.id,
            title=request.message[:50] + "..." if len(request.message) > 50 else request.message
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Save user message
    user_message = ChatMessage(
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content=request.message
    )
    db.add(user_message)
    db.commit()

    # Embed query
    query_embedding = create_embedding(request.message)

    # Search for relevant chunks
    video_id_str = str(request.video_id) if request.video_id else None
    search_results = search(
        query_embedding=query_embedding,
        user_id=str(user.id),
        video_id=video_id_str,
        limit=10
    )

    # Get top 5 results
    top_results = search_results[:5]

    # Prepare context with metadata
    context_chunks = []
    citations = []

    for result in top_results:
        payload = result.payload
        video = db.query(Video).filter(Video.id == payload["video_id"]).first()

        chunk_text = f"[Video: {video.title if video else 'Unknown'} @ {format_timestamp(payload['start_time'])}] {payload['text']}"
        context_chunks.append(chunk_text)

        # Create citation object
        citation_data = {
            "video_id": payload["video_id"],
            "video_title": video.title if video else "Unknown",
            "start_time": payload["start_time"],
            "end_time": payload["end_time"],
            "text": payload["text"]
        }
        citations.append(SourceCitation(**citation_data))

    # Construct prompt
    context = "\n".join(context_chunks)
    prompt = f"""You are a helpful AI teaching assistant. Answer the user's question based on the following video transcript chunks.

Video Transcript Context:
{context}

User Question: {request.message}

Instructions:
- Answer the question based ONLY on the provided context
- Include the video title and timestamp in your answer
- If the information is not in the context, say "I don't have information about that in the uploaded videos"
- Be concise and helpful
- Format timestamps as [Video Title @ MM:SS]
"""

    # Generate response
    response_text = generate_response(prompt)

    # Save assistant message
    assistant_message = ChatMessage(
        conversation_id=conversation.id,
        role=MessageRole.ASSISTANT,
        content=response_text,
        sources=json.dumps([c.dict() for c in citations])
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return ChatResponse(
        id=assistant_message.id,
        conversation_id=conversation.id,
        role=MessageRole.ASSISTANT,
        content=response_text,
        sources=citations,
        created_at=assistant_message.created_at
    )

@app.get("/api/chat/conversations", response_model=list[ConversationResponse])
def list_conversations(token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)

    conversations = db.query(Conversation).filter(
        Conversation.user_id == user.id
    ).order_by(Conversation.created_at.desc()).all()

    return conversations

@app.get("/api/chat/conversations/{conv_id}/messages", response_model=list[ChatResponse])
def get_messages(conv_id: str, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)

    # Verify conversation belongs to user
    conversation = db.query(Conversation).filter(
        Conversation.id == conv_id,
        Conversation.user_id == user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    messages = db.query(ChatMessage).filter(
        ChatMessage.conversation_id == conv_id
    ).order_by(ChatMessage.created_at.asc()).all()

    response_messages = []
    for msg in messages:
        sources = []
        if msg.sources:
            try:
                sources = [SourceCitation(**s) for s in json.loads(msg.sources)]
            except:
                pass

        response_messages.append(ChatResponse(
            id=msg.id,
            conversation_id=msg.conversation_id,
            role=msg.role,
            content=msg.content,
            sources=sources,
            created_at=msg.created_at
        ))

    return response_messages

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
