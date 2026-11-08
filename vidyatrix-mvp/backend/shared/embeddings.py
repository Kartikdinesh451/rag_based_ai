import requests
from config import OLLAMA_URL

def create_embedding(text: str) -> list:
    """Create embedding for a single text using BGE-M3 via Ollama"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/embed",
            json={"model": "bge-m3", "input": text},
            timeout=30
        )
        response.raise_for_status()
        return response.json()["embeddings"][0]
    except Exception as e:
        print(f"Error creating embedding: {e}")
        raise

def create_embeddings_batch(texts: list) -> list:
    """Create embeddings for multiple texts in batches"""
    all_embeddings = []
    batch_size = 50

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/embed",
                json={"model": "bge-m3", "input": batch},
                timeout=60
            )
            response.raise_for_status()
            embeddings = response.json()["embeddings"]
            all_embeddings.extend(embeddings)
        except Exception as e:
            print(f"Error creating embeddings for batch {i//batch_size}: {e}")
            raise

    return all_embeddings
