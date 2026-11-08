# Vidyatrix API Documentation

## Base URLs

- Auth API: `http://localhost:8001`
- Video API: `http://localhost:8002`
- Chat API: `http://localhost:8003`

## Authentication

All protected endpoints require a JWT token in the query parameter:
```
?token=<your_jwt_token>
```

## Auth API Endpoints

### Register User

**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-01T00:00:00"
}
```

### Login

**POST** `/auth/login`

Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### Get Current User

**GET** `/auth/me?token=<token>`

Get current authenticated user information.

**Response (200):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-01T00:00:00"
}
```

## Video API Endpoints

### Upload Video

**POST** `/api/videos/upload`

Upload a video file for processing.

**Request:** Multipart form data
- `file`: Video file (MP4, MOV, AVI, MKV, max 500MB)
- `title`: Video title
- `token`: JWT token

**Response (201):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "My Educational Video",
  "filename": "video.mp4",
  "duration": null,
  "status": "pending",
  "error_message": null,
  "created_at": "2024-01-01T00:00:00"
}
```

### List Videos

**GET** `/api/videos?token=<token>`

List all videos for the authenticated user.

**Response (200):**
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "title": "My Educational Video",
    "filename": "video.mp4",
    "duration": 120.5,
    "status": "completed",
    "error_message": null,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### Get Video

**GET** `/api/videos/{video_id}?token=<token>`

Get details of a specific video.

**Response (200):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "My Educational Video",
  "filename": "video.mp4",
  "duration": 120.5,
  "status": "completed",
  "error_message": null,
  "created_at": "2024-01-01T00:00:00"
}
```

### Delete Video

**DELETE** `/api/videos/{video_id}?token=<token>`

Delete a video and its associated data.

**Response (204):** No content

## Chat API Endpoints

### Send Chat Message

**POST** `/api/chat`

Send a message and receive AI response with citations.

**Request Body:**
```json
{
  "message": "What is this video about?",
  "video_id": "uuid (optional)",
  "conversation_id": "uuid (optional)"
}
```

**Headers:**
- `Authorization: Bearer <token>` or `?token=<token>` in query

**Response (200):**
```json
{
  "id": "uuid",
  "conversation_id": "uuid",
  "role": "assistant",
  "content": "This video is about...",
  "sources": [
    {
      "video_id": "uuid",
      "video_title": "My Educational Video",
      "start_time": 45.5,
      "end_time": 52.3,
      "text": "relevant transcript text"
    }
  ],
  "created_at": "2024-01-01T00:00:00"
}
```

### List Conversations

**GET** `/api/chat/conversations?token=<token>`

List all conversations for the authenticated user.

**Response (200):**
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "title": "What is this video about?",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### Get Conversation Messages

**GET** `/api/chat/conversations/{conversation_id}/messages?token=<token>`

Get all messages in a conversation.

**Response (200):**
```json
[
  {
    "id": "uuid",
    "conversation_id": "uuid",
    "role": "user",
    "content": "What is this video about?",
    "sources": [],
    "created_at": "2024-01-01T00:00:00"
  },
  {
    "id": "uuid",
    "conversation_id": "uuid",
    "role": "assistant",
    "content": "This video is about...",
    "sources": [
      {
        "video_id": "uuid",
        "video_title": "My Educational Video",
        "start_time": 45.5,
        "end_time": 52.3,
        "text": "relevant transcript text"
      }
    ],
    "created_at": "2024-01-01T00:00:00"
  }
]
```

## Error Responses

All endpoints may return error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid token"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created
- `204 No Content` - Successful deletion
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Rate Limiting

Currently not implemented in MVP. Future versions will include rate limiting.

## CORS

All endpoints allow CORS from any origin for development. Production should restrict origins.
