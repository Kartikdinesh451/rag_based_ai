# Vidyatrix AI SaaS - MVP

**Intelligence That Transforms Learning**

A video-only AI learning assistant that allows users to upload educational videos and ask questions with timestamped answers.

## Features

- **Video Upload**: Upload MP4, MOV, AVI, MKV videos (up to 500MB)
- **AI Transcription**: Automatic transcription using OpenAI Whisper
- **Semantic Search**: BGE-M3 embeddings for intelligent retrieval
- **AI Chat**: Ask questions and get timestamped answers
- **User Authentication**: Secure JWT-based authentication
- **Multi-Service Architecture**: Microservices for scalability

## Architecture

### Services
- **Auth API** (Port 8001): User authentication and management
- **Video API** (Port 8002): Video upload and management
- **Chat API** (Port 8003): RAG chat and retrieval
- **Worker**: Background video processing
- **Frontend** (Port 3000): React TypeScript application

### Technology Stack
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **AI/ML**: Whisper, BGE-M3, DeepSeek-R1 via Ollama
- **Vector DB**: Qdrant
- **Frontend**: React, TypeScript, Tailwind CSS, TanStack Query
- **Infrastructure**: Docker, Docker Compose

## Quick Start

### Prerequisites

1. **Docker and Docker Compose**
   ```bash
   docker --version
   docker-compose --version
   ```

2. **Ollama** with required models
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull bge-m3
   ollama pull deepseek-r1:1.5b
   ```

### Start Services

```bash
cd vidyatrix-mvp
docker-compose up -d
```

This will start:
- PostgreSQL (port 5432)
- Qdrant (port 6333)
- Auth API (port 8001)
- Video API (port 8002)
- Chat API (port 8003)
- Worker (background processing)
- Frontend (port 3000)

### Run Database Migrations

```bash
docker-compose exec auth-api python -c "
import sys
sys.path.insert(0, '/app/shared')
from alembic.config import Config
from alembic import command
alembic_cfg = Config('/app/shared/alembic.ini')
command.upgrade(alembic_cfg, 'head')
"
```

### Access the Application

- **Frontend**: http://localhost:3000
- **Auth API**: http://localhost:8001
- **Video API**: http://localhost:8002
- **Chat API**: http://localhost:8003
- **API Docs**: http://localhost:8001/docs

## Usage

1. **Register**: Create an account at http://localhost:3000/register
2. **Login**: Sign in with your credentials
3. **Upload Video**: Go to Dashboard and upload a video
4. **Wait for Processing**: The worker will transcribe and index the video
5. **Chat**: Go to Chat page and ask questions about your video

## Development

### Local Development (without Docker)

#### Backend Services

Each service can be run independently:

```bash
# Install dependencies
cd backend/auth-api
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://vidyatrix:vidyatrix_dev@localhost:5432/vidyatrix
export JWT_SECRET=dev-secret

# Run service
python main.py
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Database Setup

```bash
# Create database
createdb vidyatrix

# Run migrations
cd backend/shared
alembic upgrade head
```

## API Documentation

### Auth API
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user

### Video API
- `POST /api/videos/upload` - Upload video
- `GET /api/videos` - List user's videos
- `GET /api/videos/{id}` - Get video details
- `DELETE /api/videos/{id}` - Delete video

### Chat API
- `POST /api/chat` - Send chat message
- `GET /api/chat/conversations` - List conversations
- `GET /api/chat/conversations/{id}/messages` - Get conversation messages

## Project Structure

```
vidyatrix-mvp/
├── backend/
│   ├── auth-api/          # Authentication service
│   ├── video-api/         # Video management service
│   ├── chat-api/          # Chat and RAG service
│   ├── worker/            # Background processing
│   └── shared/            # Shared code (models, utils)
├── frontend/              # React TypeScript app
├── docker-compose.yml     # Docker orchestration
└── docs/                  # Documentation
```

## Environment Variables

See `.env.example` for required environment variables:

- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET` - JWT signing secret
- `QDRANT_URL` - Qdrant vector database URL
- `OLLAMA_URL` - Ollama API URL
- `UPLOAD_DIR` - Video upload directory

## Known Limitations (MVP)

- Video-only support (no PDF, audio, documents)
- Simple polling for background jobs
- No chat history persistence across sessions
- Basic vector search (no reranking)
- No analytics dashboard
- No admin panel
- Local storage only (no S3)
- Basic error handling

## Future Enhancements

- [ ] PDF and document support
- [ ] Notes generator
- [ ] Quiz generator
- [ ] Learning analytics
- [ ] Admin dashboard
- [ ] Hybrid search (BM25 + vector)
- [ ] Cross-encoder reranking
- [ ] S3/Cloud storage
- [ ] Redis caching
- [ ] Real-time collaboration

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs <service-name>

# Restart services
docker-compose restart
```

### Ollama connection issues
Ensure Ollama is running:
```bash
ollama serve
```

### Database connection issues
Check PostgreSQL is healthy:
```bash
docker-compose ps postgres
```

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.
