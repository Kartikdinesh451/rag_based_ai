# Vidyatrix Architecture

## System Overview

Vidyatrix is a microservices-based AI SaaS platform for video learning assistance.

## Architecture Diagram

```mermaid
graph TB
    User[User Browser] --> Frontend[React Frontend :3000]
    Frontend --> AuthAPI[Auth API :8001]
    Frontend --> VideoAPI[Video API :8002]
    Frontend --> ChatAPI[Chat API :8003]

    AuthAPI --> PostgreSQL[(PostgreSQL)]
    VideoAPI --> PostgreSQL
    ChatAPI --> PostgreSQL

    VideoAPI --> Worker[Worker Service]
    Worker --> Qdrant[(Qdrant Vector DB)]
    Worker --> Ollama[Ollama :11434]

    ChatAPI --> Qdrant
    ChatAPI --> Ollama

    style Frontend fill:#e1f5ff
    style AuthAPI fill:#fff4e1
    style VideoAPI fill:#fff4e1
    style ChatAPI fill:#fff4e1
    style Worker fill:#e1ffe1
    style PostgreSQL fill:#f0f0f0
    style Qdrant fill:#f0f0f0
    style Ollama fill:#ffe1e1
```

## Data Flow

### Video Upload Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant VideoAPI
    participant PostgreSQL
    participant Worker
    participant Qdrant
    participant Ollama

    User->>Frontend: Upload video
    Frontend->>VideoAPI: POST /api/videos/upload
    VideoAPI->>PostgreSQL: Create video record (status: pending)
    VideoAPI->>Frontend: Return video ID
    VideoAPI-->>Worker: Poll for pending videos
    Worker->>PostgreSQL: Get pending video
    Worker->>Worker: Extract audio (FFmpeg)
    Worker->>Ollama: Transcribe (Whisper)
    Worker->>Worker: Chunk transcript
    Worker->>Ollama: Generate embeddings (BGE-M3)
    Worker->>Qdrant: Store vectors
    Worker->>PostgreSQL: Update status (completed)
```

### Chat Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant ChatAPI
    participant Qdrant
    participant Ollama

    User->>Frontend: Ask question
    Frontend->>ChatAPI: POST /api/chat
    ChatAPI->>Ollama: Embed query (BGE-M3)
    ChatAPI->>Qdrant: Search similar chunks
    Qdrant-->>ChatAPI: Return top-k chunks
    ChatAPI->>ChatAPI: Construct prompt with context
    ChatAPI->>Ollama: Generate response (DeepSeek)
    Ollama-->>ChatAPI: Return answer
    ChatAPI->>Frontend: Return response with citations
    Frontend->>User: Display answer
```

## Service Responsibilities

### Auth API
- User registration and authentication
- JWT token generation and validation
- User profile management
- Token-based authorization

### Video API
- Video upload handling
- File validation (type, size)
- Video metadata storage
- Video listing and deletion
- User data isolation

### Chat API
- Chat message handling
- Query embedding
- Vector similarity search
- LLM response generation
- Citation formatting
- Conversation management

### Worker Service
- Polls for pending videos
- Audio extraction (FFmpeg)
- Speech-to-text (Whisper)
- Transcript chunking
- Embedding generation
- Vector storage
- Status updates

### Frontend
- User interface
- Authentication flow
- Video upload UI
- Chat interface
- Citation display

## Technology Choices

### Backend Framework: FastAPI
- Fast and modern
- Automatic API documentation
- Type hints support
- Async support

### Database: PostgreSQL
- Reliable and mature
- ACID compliance
- JSON support
- Excellent tooling

### Vector Database: Qdrant
- Fast vector search
- Easy to use
- Docker support
- HNSW indexing

### AI Models
- **Whisper**: Speech-to-text (OpenAI)
- **BGE-M3**: Embeddings (via Ollama)
- **DeepSeek-R1**: LLM (via Ollama)

### Frontend: React + TypeScript
- Component-based
- Type safety
- Large ecosystem
- TanStack Query for data fetching

## Data Models

### User
- id (UUID)
- email (unique)
- hashed_password
- name
- created_at

### Video
- id (UUID)
- user_id (FK)
- title
- filename
- file_path
- duration
- status (enum)
- error_message
- created_at

### TranscriptChunk
- id (UUID)
- video_id (FK)
- start_time
- end_time
- text
- created_at

### Conversation
- id (UUID)
- user_id (FK)
- title
- created_at

### ChatMessage
- id (UUID)
- conversation_id (FK)
- role (enum)
- content
- sources (JSON)
- created_at

## Security

### Authentication
- JWT access tokens
- Password hashing (bcrypt)
- Token expiration (24 hours)

### Authorization
- User-level data isolation
- Token validation on all endpoints
- Role-based access (future)

### Data Protection
- SQL injection prevention (SQLAlchemy)
- File upload validation
- CORS configuration
- Environment variable management

## Scalability Considerations

### Current MVP Limitations
- Simple polling for background jobs
- No caching layer
- Single database instance
- Local file storage

### Future Improvements
- Redis for caching and job queue
- RabbitMQ for message queuing
- Database read replicas
- S3/Cloud storage
- CDN for static assets
- Load balancing
