FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared module
COPY ../shared /app/shared

# Copy application code
COPY . .

# Create upload directory
RUN mkdir -p /app/uploads

# Expose port (not really needed for worker)
EXPOSE 8000

# Run the worker
CMD ["python", "main.py"]
