# Vidyatrix

**AI-Powered Multimodal Learning Assistant**

Vidyatrix is an intelligent learning platform that transforms educational content into interactive, AI-powered learning experiences. Upload videos, get automatic transcriptions, and ask questions with timestamped answers powered by Retrieval-Augmented Generation (RAG).

---

## 🎯 Project Overview

Vidyatrix leverages state-of-the-art AI models to create a seamless learning experience:

- **Video Understanding**: Automatic transcription with faster-whisper
- **Semantic Search**: BGE-M3 embeddings for intelligent content retrieval
- **AI-Powered Q&A**: DeepSeek-R1 generates accurate, context-aware answers
- **Timestamped Citations**: Every answer references the exact moment in the video
- **User Isolation**: Personalized learning spaces for each user

### Current Status: MVP (Video-Only)

The current implementation focuses on video-based learning as the foundation for a future multimodal platform.

---

## ✨ Key Features

### Core Functionality
- ✅ **Video Upload**: Support for MP4, MOV, AVI, MKV formats (up to 500MB)
- ✅ **AI Transcription**: Automatic speech-to-text with faster-whisper
- ✅ **Timestamped Chunks**: Transcript segmented with precise timing
- ✅ **Semantic Search**: Vector-based retrieval using BGE-M3 embeddings
- ✅ **AI Chat**: Ask questions and get answers with video timestamps
- ✅ **User Authentication**: Secure JWT-based authentication with PBKDF2 password hashing
- ✅ **Chat History**: Persistent conversation storage
- ✅ **User Data Isolation**: Each user sees only their own content

### Platform Features
- ✅ **Microservices Architecture**: Scalable service-based design
- ✅ **Docker Orchestration**: Complete containerized deployment
- ✅ **RESTful APIs**: Well-documented API endpoints
- ✅ **Modern Frontend**: React TypeScript with Tailwind CSS
- ✅ **Vector Database**: Qdrant for high-performance similarity search
- ✅ **Relational Database**: PostgreSQL for structured data persistence

---

## 🛠 Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **Vector Database**: Qdrant
- **Authentication**: JWT with PBKDF2-SHA256 password hashing
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic

### AI/ML
- **Speech-to-Text**: faster-whisper (base model)
- **Embeddings**: BGE-M3 (via Ollama)
- **LLM**: DeepSeek-R1 1.5B (via Ollama)
- **Audio Processing**: FFmpeg

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: TanStack Query
- **Routing**: React Router
- **HTTP Client**: Fetch API

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Web Server**: Nginx (frontend)

---

## 🏗 System Architecture

### Microservices Design

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                            │
│                    (React + TypeScript)                      │
│                         Port 3000                            │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Auth API    │ │  Video API   │ │  Chat API    │
│   Port 8001  │ │   Port 8002  │ │   Port 8003  │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                 │                │
       └─────────────────┼────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  PostgreSQL  │ │    Qdrant    │ │   Worker     │
│   Port 5432  │ │  Port 6333   │ │  Background  │
└──────────────┘ └──────┬───────┘ └──────┬───────┘
                       │                │
                       └────────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │    Ollama    │
                         │   Port 11434 │
                         └──────────────┘
```

### Data Flow

**Video Processing Pipeline:**
1. User uploads video → Video API stores file
2. Worker polls for pending videos
3. Worker extracts audio with FFmpeg
4. faster-whisper transcribes audio
5. Transcript chunked into 30-second segments
6. BGE-M3 generates embeddings for each chunk
7. Vectors stored in Qdrant with metadata
8. Database updated with "completed" status

**Chat Pipeline:**
1. User asks question → Chat API receives query
2. BGE-M3 generates query embedding
3. Qdrant searches for similar chunks (top-5)
4. Context built from retrieved chunks
5. DeepSeek-R1 generates answer
6. Response with citations returned to user
7. Conversation saved to database

---

## 📁 Repository Structure

```
vidyatrix-mvp/
├── backend/
│   ├── auth-api/              # Authentication service
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   └── requirements.txt
│   ├── video-api/             # Video management service
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   └── requirements.txt
│   ├── chat-api/              # Chat and RAG service
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   └── requirements.txt
│   ├── worker/                # Background processing
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   └── requirements.txt
│   └── shared/                # Shared code modules
│       ├── __init__.py
│       ├── alembic/           # Database migrations
│       │   ├── versions/
│       │   │   └── 001_initial_migration.py
│       │   ├── env.py
│       │   └── script.py.mako
│       ├── alembic.ini
│       ├── config.py          # Configuration
│       ├── database.py        # Database connection
│       ├── embeddings.py      # BGE-M3 embeddings
│       ├── models.py          # SQLAlchemy models
│       ├── qdrant_helper.py   # Qdrant operations
│       ├── schemas.py         # Pydantic schemas
│       └── security.py        # JWT and password hashing
├── frontend/                  # React TypeScript application
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── index.html
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── index.css
│       ├── lib/
│       │   ├── api.ts         # API client
│       │   └── utils.ts       # Utility functions
│       └── pages/
│           ├── LoginPage.tsx
│           ├── RegisterPage.tsx
│           ├── Dashboard.tsx
│           └── ChatPage.tsx
├── docs/                      # Documentation
│   ├── API.md                 # API documentation
│   ├── ARCHITECTURE.md        # System architecture
│   └── DEVELOPMENT_SUMMARY.md  # Development notes
├── docker-compose.yml         # Docker orchestration
├── .env.example              # Environment variables template
├── .gitignore
├── README.md
└── SETUP_GUIDE.md            # Detailed setup instructions
```

---

## 🚀 Installation

### Prerequisites

1. **Docker Desktop** (v20.10+)
   - Download from [docker.com](https://www.docker.com/products/docker-desktop)
   - Ensure Docker and Docker Compose are installed

2. **Ollama** (for local AI models)
   - Download from [ollama.ai](https://ollama.ai)
   - Install and start Ollama

3. **Required Ollama Models**
   ```bash
   ollama pull bge-m3
   ollama pull deepseek-r1:1.5b
   ```

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kartikdinesh451/rag_based_ai.git
   cd rag_based_ai/vidyatrix-mvp
   ```

2. **Start Ollama**
   ```bash
   ollama serve
   ```

3. **Start all services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

   This will start:
   - PostgreSQL (port 5432)
   - Qdrant (ports 6333-6334)
   - Auth API (port 8001)
   - Video API (port 8002)
   - Chat API (port 8003)
   - Worker (background processing)
   - Frontend (port 3000)

4. **Run database migrations**
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

5. **Access the application**
   - Frontend: http://localhost:3000
   - Auth API: http://localhost:8001
   - Video API: http://localhost:8002
   - Chat API: http://localhost:8003
   - API Docs: http://localhost:8001/docs

---

## ⚙️ Environment Variables

Create a `.env` file in the project root (see `.env.example`):

```env
# Database
DATABASE_URL=postgresql://vidyatrix:vidyatrix_dev@postgres:5432/vidyatrix

# Authentication
JWT_SECRET=your-secret-key-change-in-production

# Vector Database
QDRANT_URL=http://qdrant:6333

# AI Models
OLLAMA_URL=http://host.docker.internal:11434

# File Upload
UPLOAD_DIR=/app/uploads
```

**Note:** The docker-compose.yml includes default development values. Change these for production deployment.

---

## 💻 Local Development

### Backend Development

Each service can be run independently for development:

```bash
# Install dependencies
cd backend/auth-api
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://vidyatrix:vidyatrix_dev@localhost:5432/vidyatrix
export JWT_SECRET=dev-secret
export QDRANT_URL=http://localhost:6333
export OLLAMA_URL=http://localhost:11434

# Run service
python main.py
```

Repeat for other services (video-api, chat-api, worker).

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:5173

### Database Setup (Local)

```bash
# Create database
createdb vidyatrix

# Run migrations
cd backend/shared
alembic upgrade head
```

---

## 📚 API Documentation

### Authentication

All protected endpoints require a JWT token:
- As query parameter: `?token=<your_jwt_token>`
- Services validate token on each request

### Auth API (Port 8001)

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and receive JWT token
- `GET /health` - Health check

### Video API (Port 8002)

- `POST /api/videos/upload` - Upload video (max 500MB)
- `GET /api/videos` - List user's videos
- `GET /api/videos/{id}` - Get video details
- `DELETE /api/videos/{id}` - Delete video
- `GET /health` - Health check

### Chat API (Port 8003)

- `POST /api/chat` - Send chat message with RAG
- `GET /api/chat/conversations` - List conversations
- `GET /api/chat/conversations/{id}/messages` - Get conversation history
- `GET /health` - Health check

**Full API Documentation:** See [docs/API.md](docs/API.md)

---

## 🧪 Testing

### Manual Testing

1. **Registration**
   ```bash
   curl -X POST http://localhost:8001/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"test123","name":"Test User"}'
   ```

2. **Login**
   ```bash
   curl -X POST http://localhost:8001/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"test123"}'
   ```

3. **Video Upload**
   - Use the frontend at http://localhost:3000
   - Or via API with curl (requires JWT token)

4. **Chat**
   - Use the frontend Chat page
   - Or via API with the chat endpoint

### Automated Testing

**Note:** Automated tests are not included in the MVP scope. This is planned for future development.

---

## 🔒 Security

### Implemented Security Measures

- ✅ **Password Hashing**: PBKDF2-SHA256 (no 72-byte limit like bcrypt)
- ✅ **JWT Authentication**: Token-based auth with 24-hour expiration
- ✅ **User Data Isolation**: Each user sees only their own data
- ✅ **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries
- ✅ **File Upload Validation**: Type and size validation (max 500MB)
- ✅ **CORS Configuration**: Configured for development (restrict for production)
- ✅ **Environment Variables**: Secrets managed via environment variables

### Production Security Checklist

Before deploying to production:

- [ ] Change `JWT_SECRET` to a strong random value
- [ ] Change PostgreSQL password from development default
- [ ] Restrict CORS to specific domains
- [ ] Enable HTTPS/SSL
- [ ] Implement rate limiting on API endpoints
- [ ] Add request logging and monitoring
- [ ] Set up database backups
- [ ] Configure firewall rules
- [ ] Use secrets management (e.g., AWS Secrets Manager, HashiCorp Vault)

---

## 🚀 Deployment

### Docker Deployment

The application is fully containerized and ready for Docker-based deployment:

```bash
# Build and start services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Considerations

1. **Environment Variables**: Use production values for secrets
2. **Persistence**: Configure Docker volumes for PostgreSQL and Qdrant
3. **Scaling**: Use Kubernetes or Docker Swarm for horizontal scaling
4. **Load Balancing**: Add a load balancer (nginx, Traefik) for API services
5. **Monitoring**: Implement Prometheus/Grafana for monitoring
6. **Logging**: Use centralized logging (ELK stack, Loki)
7. **SSL/TLS**: Configure SSL certificates for HTTPS

### Cloud Deployment

The application can be deployed to:
- AWS (ECS, EKS)
- Google Cloud (GKE, Cloud Run)
- Azure (AKS, Container Instances)
- DigitalOcean (App Platform, Kubernetes)
- Heroku (with container registry)

---

## 📸 Screenshots

*Note: Screenshots should be added here after capturing the actual application UI.*

### Dashboard
![Dashboard](assets/screenshots/dashboard.png)

### Chat Interface
![Chat](assets/screenshots/chat.png)

### Video Upload
![Upload](assets/screenshots/upload.png)

---

## 🗺 Roadmap

### MVP (Current - ✅ Complete)
- [x] Video upload and management
- [x] AI transcription with faster-whisper
- [x] BGE-M3 embeddings
- [x] RAG chat with DeepSeek-R1
- [x] Timestamped answers
- [x] User authentication
- [x] User data isolation
- [x] Docker orchestration

### Phase 2: Enhanced Features (Planned)
- [ ] PDF document support
- [ ] Audio file support
- [ ] Notes generator
- [ ] Quiz generator
- [ ] Enhanced citation display
- [ ] Clickable timestamps for video navigation
- [ ] Chat export functionality

### Phase 3: Platform Features (Planned)
- [ ] Learning analytics dashboard
- [ ] Progress tracking
- [ ] Bookmarking and highlighting
- [ ] Collaborative learning
- [ ] User profiles and settings
- [ ] Subscription management

### Phase 4: Advanced AI (Planned)
- [ ] Hybrid search (BM25 + vector)
- [ ] Cross-encoder reranking
- [ ] Multi-modal RAG (text + video frames)
- [ ] Answer validation
- [ ] Personalized learning paths

### Phase 5: Infrastructure (Planned)
- [ ] Redis caching
- [ ] RabbitMQ message queue
- [ ] S3/Cloud storage integration
- [ ] CDN for static assets
- [ ] Database read replicas
- [ ] Rate limiting
- [ ] Admin panel

---

## 🐛 Troubleshooting

### Services won't start

```bash
# Check Docker logs
docker-compose logs <service-name>

# Restart specific service
docker-compose restart <service-name>

# Rebuild and restart
docker-compose up -d --build <service-name>
```

### Ollama connection issues

Ensure Ollama is running:
```bash
ollama serve
```

Verify models are downloaded:
```bash
ollama list
```

### Database connection issues

Check PostgreSQL health:
```bash
docker-compose ps postgres
docker-compose logs postgres
```

### Video processing stuck

Check worker logs:
```bash
docker-compose logs worker
```

Manually trigger processing by updating video status to "pending" in database.

### Frontend build errors

Clear node_modules and reinstall:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation in `/docs`
- Review API documentation in `docs/API.md`

---

## 🙏 Acknowledgments

- **faster-whisper** - Speech-to-text transcription
- **BGE-M3** - Embedding model
- **DeepSeek-R1** - Large language model
- **Ollama** - Local AI model runtime
- **Qdrant** - Vector database
- **FastAPI** - Modern Python web framework
- **React** - JavaScript library for building UIs

---

**Project Status**: MVP - Video-Only AI Learning Assistant  
**Last Updated**: November 2026  
**Version**: 1.0.0
