# Vidyatrix – AI-Powered Multimodal Learning Assistant

> **RAG-based question answering, document intelligence, video understanding and personalized learning tools.**

---

## 🚀 Quick Start

The main Vidyatrix AI SaaS application is located in the `vidyatrix-mvp/` directory.

### Vidyatrix MVP (Current Release)

**Prerequisites:**
- Docker Desktop installed and running
- Ollama installed with required models

**Step 1: Install Ollama Models**

```bash
ollama pull bge-m3
ollama pull deepseek-r1:1.5b
```

**Step 2: Start Ollama**

```bash
ollama serve
```

**Step 3: Start Vidyatrix Services**

```bash
cd vidyatrix-mvp
docker compose up -d
```

**Step 4: Run Database Migrations**

```bash
docker compose exec auth-api python -c "import sys; sys.path.insert(0, '/app/shared'); from alembic.config import Config; from alembic import command; command.upgrade(Config('/app/shared/alembic.ini'), 'head')"
```

**Step 5: Access the Application**

- Frontend: http://localhost:3000
- Auth API: http://localhost:8001
- Video API: http://localhost:8002
- Chat API: http://localhost:8003
- API Docs: http://localhost:8001/docs

**See [vidyatrix-mvp/README.md](vidyatrix-mvp/README.md) for complete documentation.**

---

## 📁 Repository Structure

```
rag_based_ai/
├── vidyatrix-mvp/          # Main Vidyatrix AI SaaS application
│   ├── backend/            # Microservices (Auth, Video, Chat, Worker)
│   ├── frontend/           # React TypeScript application
│   ├── docker-compose.yml  # Docker orchestration
│   └── README.md           # Complete documentation
│
├── src/                    # Original RAG scripts (legacy)
├── videos/                 # Video storage (legacy)
├── audios/                 # Audio storage (legacy)
├── jsons/                  # Transcript JSONs (legacy)
└── docs/                   # Legacy documentation
```

---

## 🎯 Vidyatrix MVP Overview

Vidyatrix is a modern, microservices-based AI learning assistant that transforms educational videos into interactive learning experiences.

### Key Features (Video-Only MVP)

- ✅ Video upload and management (MP4, MOV, AVI, MKV up to 500MB)
- ✅ AI transcription with faster-whisper
- ✅ Semantic search with BGE-M3 embeddings
- ✅ RAG chat with DeepSeek-R1
- ✅ Timestamped answers with citations
- ✅ User authentication with JWT
- ✅ User data isolation
- ✅ Chat history persistence
- ✅ Docker-based deployment

### Technology Stack

**Backend:**
- FastAPI (Python 3.11)
- PostgreSQL 15
- Qdrant Vector Database
- SQLAlchemy ORM
- Alembic Migrations

**AI/ML:**
- faster-whisper (speech-to-text)
- BGE-M3 (embeddings via Ollama)
- DeepSeek-R1 1.5B (LLM via Ollama)
- FFmpeg (audio processing)

**Frontend:**
- React 18 with TypeScript
- Vite (build tool)
- Tailwind CSS
- TanStack Query
- React Router

**Infrastructure:**
- Docker
- Docker Compose
- Nginx (frontend web server)

**Full documentation:** [vidyatrix-mvp/README.md](vidyatrix-mvp/README.md)

---

## 📚 Legacy RAG Scripts

The `src/` directory contains the original RAG-based teaching assistant scripts that demonstrate the core concepts:

- `video_to_mp3.py` - Video to audio conversion
- `speech_to_text.py` - Whisper transcription
- `preprocess_json.py` - Embedding generation
- `process_incoming.py` - RAG query processing

**Note:** These scripts are preserved for reference but are superseded by the Vidyatrix MVP implementation.

---

## 🛠 Installation

### Prerequisites

**Required:**
- Docker Desktop (v20.10 or later)
- Ollama (latest version)

**System Requirements:**
- Windows 10/11, macOS, or Linux
- 8GB RAM minimum (16GB recommended)
- 20GB disk space for Docker images

### Vidyatrix MVP Setup

**Windows 11 (PowerShell):**

```powershell
# Navigate to project directory
cd vidyatrix-mvp

# Start Docker Desktop if not running
# Start Ollama
ollama serve

# Pull required models (in separate terminal)
ollama pull bge-m3
ollama pull deepseek-r1:1.5b

# Start all services
docker compose up -d

# Run database migrations
docker compose exec auth-api python -c "import sys; sys.path.insert(0, '/app/shared'); from alembic.config import Config; from alembic import command; command.upgrade(Config('/app/shared/alembic.ini'), 'head')"

# Access the application
# Open http://localhost:3000 in your browser
```

**macOS/Linux:**

```bash
# Navigate to project directory
cd vidyatrix-mvp

# Start Ollama
ollama serve

# Pull required models (in separate terminal)
ollama pull bge-m3
ollama pull deepseek-r1:1.5b

# Start all services
docker compose up -d

# Run database migrations
docker compose exec auth-api python -c "import sys; sys.path.insert(0, '/app/shared'); from alembic.config import Config; from alembic import command; command.upgrade(Config('/app/shared/alembic.ini'), 'head')"

# Access the application
# Open http://localhost:3000 in your browser
```

**Access URLs:**
- Frontend: http://localhost:3000
- Auth API: http://localhost:8001
- Video API: http://localhost:8002
- Chat API: http://localhost:8003
- API Documentation: http://localhost:8001/docs
- Qdrant Dashboard: http://localhost:6333/dashboard

### Legacy Scripts Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install and start Ollama
ollama serve

# Pull required models
ollama pull bge-m3
ollama pull deepseek-r1:1.5b
```

---

## 📖 Documentation

- **Vidyatrix MVP**: [vidyatrix-mvp/README.md](vidyatrix-mvp/README.md)
- **API Documentation**: [vidyatrix-mvp/docs/API.md](vidyatrix-mvp/docs/API.md)
- **Architecture**: [vidyatrix-mvp/docs/ARCHITECTURE.md](vidyatrix-mvp/docs/ARCHITECTURE.md)
- **Setup Guide**: [vidyatrix-mvp/SETUP_GUIDE.md](vidyatrix-mvp/SETUP_GUIDE.md)

---

## 🔧 Troubleshooting

### Docker Issues

**Docker not starting:**
```bash
# Check Docker Desktop is running
docker --version
docker compose version
```

**Services won't start:**
```bash
# Check service logs
docker compose logs

# Restart services
docker compose restart

# Rebuild and restart
docker compose up -d --build
```

### Ollama Issues

**Ollama connection failed:**
```bash
# Ensure Ollama is running
ollama serve

# Verify models are installed
ollama list
```

### Database Issues

**Migration failed:**
```bash
# Check PostgreSQL is healthy
docker compose ps postgres

# View PostgreSQL logs
docker compose logs postgres

# Retry migration
docker compose exec auth-api python -c "import sys; sys.path.insert(0, '/app/shared'); from alembic.config import Config; from alembic import command; command.upgrade(Config('/app/shared/alembic.ini'), 'head')"
```

### Port Conflicts

If ports are already in use, modify `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # Change frontend port
  - "8002:8001"  # Change auth API port
```

---

## 🤝 Contributing

Contributions are welcome! Please see [vidyatrix-mvp/README.md](vidyatrix-mvp/README.md) for contribution guidelines.

---

## 📄 License

MIT License

---

## 🎯 Current Status

**Project**: Vidyatrix – AI-Powered Multimodal Learning Assistant  
**Status**: MVP Release (Video-Only)  
**Version**: 1.0.0  
**Repository**: https://github.com/Kartikdinesh451/rag_based_ai

### MVP Scope (Current Release)

**Implemented:**
- ✅ Video upload and processing
- ✅ AI transcription with faster-whisper
- ✅ Semantic search with BGE-M3
- ✅ RAG chat with DeepSeek-R1
- ✅ User authentication
- ✅ Docker deployment

**Not Implemented (Future Roadmap):**
- ❌ PDF document support
- ❌ Audio file support
- ❌ Notes generator
- ❌ Quiz generator
- ❌ Analytics dashboard
- ❌ Admin panel
- ❌ S3/Cloud storage
- ❌ Redis caching

---

## 🙏 Acknowledgments

- **faster-whisper** - Speech-to-text transcription
- **BGE-M3** - Embedding model
- **DeepSeek-R1** - Large language model
- **Ollama** - Local AI model runtime
- **Qdrant** - Vector database
- **FastAPI** - Modern Python web framework
- **React** - JavaScript library for building UIs
