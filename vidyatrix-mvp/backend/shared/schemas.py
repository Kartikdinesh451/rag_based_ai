from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from .models import VideoStatus, MessageRole

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Video Schemas
class VideoCreate(BaseModel):
    title: str

class VideoResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    filename: str
    duration: Optional[float]
    status: VideoStatus
    error_message: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Chat Schemas
class ChatRequest(BaseModel):
    message: str
    video_id: Optional[UUID] = None
    conversation_id: Optional[UUID] = None

class SourceCitation(BaseModel):
    video_id: UUID
    video_title: str
    start_time: float
    end_time: float
    text: str

class ChatResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    role: MessageRole
    content: str
    sources: List[SourceCitation]
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationCreate(BaseModel):
    title: str

class ConversationResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    created_at: datetime

    class Config:
        from_attributes = True
