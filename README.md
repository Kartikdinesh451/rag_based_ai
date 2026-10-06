# 🎓 RAG-Based AI Teaching Assistant

A Retrieval-Augmented Generation (RAG) teaching assistant that answers questions from course-video content and guides the learner to the relevant video and timestamp.

> **Code-preservation rule:** the supplied project code has been copied without changing its logic. This package adds GitHub organization, documentation, screenshots and placeholders only.

## 🚀 Project overview

**Video → MP3 → Whisper transcription → timestamped JSON → embeddings → semantic retrieval → LLM response**

### Technologies used
- **Whisper `large-v2`** — speech-to-text
- **Ollama `bge-m3`** — embeddings
- **Cosine similarity** — semantic retrieval
- **Ollama `deepseek-r1:1.5b`** — response generation
- **Pandas / NumPy / Joblib / Requests / scikit-learn**

The supplied retrieval script selects the **top 5** most similar transcript chunks and sends their title, video number, timestamps and text to the LLM.

## 🧠 Architecture

```text
Course Videos
      │
      ▼
video_to_mp3.py
      │
      ▼
MP3 Audio
      │
      ▼
speech_to_text.py / mp3_to_json.py
      │
      ▼
Timestamped JSON Chunks
      │
      ▼
preprocess_json.py
      │
      ▼
bge-m3 Embeddings
      │
      ▼
embeddings.joblib
      │
      ▼
process_incoming.py
      │
      ├── User question
      ├── bge-m3 question embedding
      ├── Cosine similarity
      └── Top 5 transcript chunks
              │
              ▼
       DeepSeek R1 1.5B
              │
              ▼
   Answer + video/timestamp guidance
```

## 📁 Repository structure

The root runtime folders intentionally match the paths hard-coded in the original scripts:

```text
RAG_Based_AI/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── embeddings.joblib.placeholder
│
├── videos/                  # Add large source videos locally
├── audios/                  # Add generated MP3s locally
├── jsons/                   # Timestamped transcript JSON
│   ├── 2_Your First HTML Website.json
│   ├── 6_SEO and Core Web Vitals in HTML.json
│   └── 10_Video, Audio & Media in HTML.json
│
├── src/
│   ├── video_to_mp3.py
│   ├── speech_to_text.py
│   ├── preprocess_json.py
│   ├── process_incoming.py
│   └── ADD_mp3_to_json.py.txt
│
├── outputs/
│   ├── output.json
│   ├── prompt.txt
│   └── response.txt
│
├── assets/
│   └── project_screenshot_*.png
│
├── docs/
│   ├── PROJECT_NOTES.md
│   ├── GITHUB_CHECKLIST.md
│   └── ORIGINAL_README.md
│
└── tests/
```

## ⚙️ Setup

### Python packages

```bash
pip install -r requirements.txt
```

### External dependencies

Install **FFmpeg** for video-to-MP3 conversion.

Install and run **Ollama** locally. The supplied code calls:

```text
http://localhost:11434
```

Required models:

```bash
ollama pull bge-m3
ollama pull deepseek-r1:1.5b
```

## ▶️ Run the pipeline

### 1. Add videos

Put your course videos in:

```text
videos/
```

### 2. Convert videos to MP3

```bash
python src/video_to_mp3.py
```

The original script reads `videos/` and writes MP3 files into `audios/`.

### 3. Convert MP3 to JSON

Your screenshot shows the original `mp3_to_json.py` in the local project. Its source was not included in the uploaded files for this packaging step, so it has **not** been recreated or modified.

Copy your original file to:

```text
src/mp3_to_json.py
```

Then use your original workflow to populate:

```text
jsons/
```

### 4. Create embeddings

```bash
python src/preprocess_json.py
```

The supplied script calls Ollama's `bge-m3` embedding endpoint and saves the dataframe as:

```text
embeddings.joblib
```

### 5. Ask a question

Once `embeddings.joblib` is available:

```bash
python src/process_incoming.py
```

Enter your question at:

```text
Ask a Question:
```

The supplied code retrieves the most similar transcript chunks and asks the LLM to answer with the relevant video and timestamp.

## 🔎 Example

```text
Where is responsive design taught?
```

The retrieval stage searches the transcript embeddings and passes the most relevant timestamped chunks to the LLM.

## ⚠️ Important source-code behavior retained

I did **not** change this because you specifically asked not to modify the code.

The supplied `preprocess_json.py` contains a `break` after the first JSON file is processed. Therefore, **as currently written, it stops after the first JSON file** instead of processing every JSON file in `jsons/`.

This is documented rather than silently changed.

The original scripts also use fixed relative paths:

```text
videos/
audios/
jsons/
embeddings.joblib
```

The package keeps those exact runtime folder names so the surrounding structure matches the supplied code.

## 📦 GitHub storage recommendation

Do not upload large course videos and MP3 files into normal Git history.

Recommended:
- Keep Python source code and small JSON samples in GitHub.
- Keep large `.mp4`, `.webm` and `.mp3` files local or use Git LFS/external storage.
- Add your generated `embeddings.joblib` only if you intentionally want that artifact public.

## 📌 Portfolio title

**RAG-Based AI Teaching Assistant | Python, Whisper, Ollama, BGE-M3, DeepSeek-R1**

This project demonstrates an end-to-end RAG workflow:
**transcription → embeddings → retrieval → prompt construction → local LLM inference → timestamp-aware answer generation.**
