# Vidyatrix – AI-Powered Multimodal Learning Assistant

> **RAG-based question answering, document intelligence, video understanding and personalized learning tools.**

---

## 🚀 Quick Start

The main Vidyatrix AI SaaS application is located in the `vidyatrix-mvp/` directory.

### Vidyatrix MVP (Current Production)

```bash
cd vidyatrix-mvp
docker-compose up -d
```

Access the application at http://localhost:3000

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

### Key Features
- ✅ Video upload and management
- ✅ AI transcription with faster-whisper
- ✅ Semantic search with BGE-M3 embeddings
- ✅ RAG chat with DeepSeek-R1
- ✅ Timestamped answers with citations
- ✅ User authentication and data isolation
- ✅ Docker-based deployment

### Technology Stack
- **Backend**: FastAPI, PostgreSQL, Qdrant
- **AI**: faster-whisper, BGE-M3, DeepSeek-R1 (via Ollama)
- **Frontend**: React, TypeScript, Tailwind CSS
- **Infrastructure**: Docker, Docker Compose

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
- Docker Desktop
- Ollama with models: `bge-m3`, `deepseek-r1:1.5b`

### Vidyatrix MVP Setup

```bash
cd vidyatrix-mvp
docker-compose up -d
docker-compose exec auth-api python -c "
import sys
sys.path.insert(0, '/app/shared')
from alembic.config import Config
from alembic import command
command.upgrade(Config('/app/shared/alembic.ini'), 'head')
"
```

**Access:** http://localhost:3000

### Legacy Scripts Setup

```bash
pip install -r requirements.txt
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

## 🤝 Contributing

Contributions are welcome! Please see [vidyatrix-mvp/README.md](vidyatrix-mvp/README.md) for contribution guidelines.

---

## 📄 License

MIT License

---

**Project**: Vidyatrix – AI-Powered Multimodal Learning Assistant  
**Status**: Production MVP (Video-Only)  
**Repository**: https://github.com/Kartikdinesh451/rag_based_ai
