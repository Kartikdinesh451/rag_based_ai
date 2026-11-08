# Vidyatrix AI SaaS - Setup Guide

## Current Environment Status

✅ Python 3.11.9 - Available
✅ Node.js v22.23.2 - Available
✅ Ollama 0.40.5 - Available
❌ Docker - Not Installed
❌ Docker Compose - Not Installed

## Option 1: Install Docker (Recommended)

Docker is required to run PostgreSQL and Qdrant databases.

### Windows Installation

1. **Download Docker Desktop**
   - Go to https://www.docker.com/products/docker-desktop/
   - Download Docker Desktop for Windows
   - Run the installer

2. **Install WSL 2** (if not already installed)
   - Open PowerShell as Administrator
   - Run: `wsl --install`
   - Restart your computer

3. **Start Docker Desktop**
   - Launch Docker Desktop from Start menu
   - Wait for it to start (green icon in system tray)

4. **Verify Installation**
   ```bash
   docker --version
   docker-compose --version
   ```

### Then Run the Project

```bash
cd vidyatrix-mvp

# Start Ollama and pull models
ollama serve
# In another terminal:
ollama pull bge-m3
ollama pull deepseek-r1:1.5b

# Start Docker services
docker-compose up -d

# Run database migrations
docker-compose exec auth-api python -c "
import sys
sys.path.insert(0, '/app/shared')
from alembic.config import Config
from alembic import command
alembic_cfg = Config('/app/shared/alembic.ini')
command.upgrade(alembic_cfg, 'head')
"

# Access the application
# Frontend: http://localhost:3000
```

## Option 2: Use Local Databases (Without Docker)

If you cannot install Docker, you can use local installations of PostgreSQL and Qdrant.

### Install PostgreSQL (Windows)

1. **Download PostgreSQL**
   - Go to https://www.postgresql.org/download/windows/
   - Download and install PostgreSQL 15
   - Set password: `vidyatrix_dev`
   - Note the port (default: 5432)

2. **Create Database**
   ```bash
   # Open pgAdmin or use psql
   psql -U postgres
   CREATE DATABASE vidyatrix;
   CREATE USER vidyatrix WITH PASSWORD 'vidyatrix_dev';
   GRANT ALL PRIVILEGES ON DATABASE vidyatrix TO vidyatrix;
   ```

### Install Qdrant (Windows)

1. **Download Qdrant**
   - Go to https://github.com/qdrant/qdrant/releases
   - Download the Windows executable
   - Extract to a folder

2. **Run Qdrant**
   ```bash
   cd qdrant-folder
   .\qdrant.exe
   ```
   Qdrant will start on http://localhost:6333

### Then Run Backend Services

```bash
cd vidyatrix-mvp

# Set environment variables
set DATABASE_URL=postgresql://vidyatrix:vidyatrix_dev@localhost:5432/vidyatrix
set JWT_SECRET=dev-secret-change-in-production
set QDRANT_URL=http://localhost:6333
set OLLAMA_URL=http://localhost:11434
set UPLOAD_DIR=./uploads

# Install Python dependencies for each service
cd backend/shared
pip install -r ../auth-api/requirements.txt
pip install -r ../video-api/requirements.txt
pip install -r ../chat-api/requirements.txt
pip install -r ../worker/requirements.txt

# Run database migrations
alembic upgrade head

# Start services in separate terminals

# Terminal 1 - Auth API
cd backend/auth-api
python main.py

# Terminal 2 - Video API
cd backend/video-api
python main.py

# Terminal 3 - Chat API
cd backend/chat-api
python main.py

# Terminal 4 - Worker
cd backend/worker
python main.py

# Terminal 5 - Frontend
cd frontend
npm install
npm run dev
```

## Option 3: Use Cloud Services

You can use cloud database services instead of local installation.

### Supabase (PostgreSQL)

1. Create free account at https://supabase.com
2. Create a new project
3. Get connection string from Settings > Database
4. Update DATABASE_URL in environment

### Qdrant Cloud

1. Create free account at https://cloud.qdrant.io
2. Create a cluster
3. Get API URL
4. Update QDRANT_URL in environment

### Then Run Services

Same as Option 2, but use cloud connection strings.

## Quick Start (If You Already Have Docker)

```bash
cd vidyatrix-mvp

# Start Ollama
ollama serve
# In another terminal:
ollama pull bge-m3
ollama pull deepseek-r1:1.5b

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec auth-api python -c "
import sys
sys.path.insert(0, '/app/shared')
from alembic.config import Config
from alembic import command
alembic_cfg = Config('/app/shared/alembic.ini')
command.upgrade(alembic_cfg, 'head')
"

# Check services are running
docker-compose ps

# Access application
# Open browser: http://localhost:3000
```

## Troubleshooting

### Docker won't start
- Ensure WSL 2 is installed
- Restart Docker Desktop
- Check Windows virtualization is enabled in BIOS

### Ollama connection issues
```bash
# Check Ollama is running
ollama list

# Restart Ollama
# Stop and start again
```

### Database connection errors
- Check PostgreSQL is running
- Verify connection string
- Check firewall settings

### Port conflicts
- Change ports in docker-compose.yml if needed
- Check what's using the port: `netstat -ano | findstr :8001`

## Current Status

The project code is complete and ready to run. You need to:
1. Install Docker (recommended) OR install PostgreSQL and Qdrant locally
2. Start Ollama and pull models
3. Start the services
4. Run database migrations
5. Access the application at http://localhost:3000

## Development Workflow

Once running:
1. Register a new account
2. Login
3. Upload a video (MP4, MOV, AVI, MKV)
4. Wait for processing (status will change from "pending" to "completed")
5. Go to Chat page
6. Ask questions about the video
7. View responses with timestamped citations
