from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import sys
import os
import uuid
import shutil

# Add shared directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))

from database import get_db
from models import User, Video, VideoStatus
from schemas import VideoResponse
from security import decode_token
from config import UPLOAD_DIR

app = FastAPI(title="Video API")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "video-api"}

@app.post("/api/videos/upload", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
def upload_video(
    file: UploadFile = File(...),
    title: str = Form(...),
    token: str = Form(...),
    db: Session = Depends(get_db)
):
    # Validate token and get user
    user = get_current_user(token, db)

    # Validate file type
    if not file.filename.endswith(('.mp4', '.mov', '.avi', '.mkv')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only MP4, MOV, AVI, MKV are supported"
        )

    # Validate file size (max 500MB)
    file_size = 0
    for chunk in file.file:
        file_size += len(chunk)
        if file_size > 500 * 1024 * 1024:  # 500MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File too large. Maximum size is 500MB"
            )
    file.file.seek(0)  # Reset file pointer

    # Generate unique filename
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create video record
    video = Video(
        user_id=user.id,
        title=title,
        filename=file.filename,
        file_path=file_path,
        status=VideoStatus.PENDING
    )
    db.add(video)
    db.commit()
    db.refresh(video)

    return video

@app.get("/api/videos", response_model=list[VideoResponse])
def list_videos(token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)

    videos = db.query(Video).filter(Video.user_id == user.id).order_by(Video.created_at.desc()).all()
    return videos

@app.get("/api/videos/{video_id}", response_model=VideoResponse)
def get_video(video_id: str, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)

    video = db.query(Video).filter(
        Video.id == video_id,
        Video.user_id == user.id
    ).first()

    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )

    return video

@app.delete("/api/videos/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_video(video_id: str, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)

    video = db.query(Video).filter(
        Video.id == video_id,
        Video.user_id == user.id
    ).first()

    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )

    # Delete file
    if os.path.exists(video.file_path):
        os.remove(video.file_path)

    # Delete from database (cascade will delete transcript chunks)
    db.delete(video)
    db.commit()

    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
