# Project Notes

## Source-derived pipeline

The original project README describes five stages:
1. Collect videos.
2. Convert videos to MP3.
3. Convert MP3 files to JSON.
4. Convert JSON chunks into embeddings and save them as a Joblib artifact.
5. Load the artifact, retrieve relevant chunks for a user query, and feed the resulting prompt to an LLM.

The supplied `process_incoming.py` uses Ollama's local API, `bge-m3` embeddings, cosine similarity, top-5 retrieval and `deepseek-r1:1.5b` generation.

## Preservation

The supplied source files were copied byte-for-byte. Only their filenames were normalized for the GitHub `src/` folder.

## Known source behavior

The supplied `preprocess_json.py` contains a `break` after the first JSON file. This was retained exactly as requested.
