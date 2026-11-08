import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from .config import QDRANT_URL

client = QdrantClient(url=QDRANT_URL)
COLLECTION_NAME = "video_chunks"

def init_collection():
    """Initialize Qdrant collection for video chunks"""
    try:
        collections = client.get_collections().collections
        collection_names = [c.name for c in collections]

        if COLLECTION_NAME not in collection_names:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
            )
            print(f"Created collection: {COLLECTION_NAME}")
        else:
            print(f"Collection {COLLECTION_NAME} already exists")
    except Exception as e:
        print(f"Error initializing collection: {e}")
        raise

def upsert_chunks(chunks: list):
    """Upsert video chunks to Qdrant"""
    points = []
    for i, chunk in enumerate(chunks):
        point = PointStruct(
            id=chunk["id"],
            vector=chunk["embedding"],
            payload={
                "user_id": str(chunk["user_id"]),
                "video_id": str(chunk["video_id"]),
                "start_time": chunk["start_time"],
                "end_time": chunk["end_time"],
                "text": chunk["text"]
            }
        )
        points.append(point)

    try:
        client.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f"Upserted {len(points)} chunks to Qdrant")
    except Exception as e:
        print(f"Error upserting chunks: {e}")
        raise

def search(query_embedding: list, user_id: str, video_id: str = None, limit: int = 10):
    """Search for similar chunks"""
    try:
        # Build filter
        conditions = [
            FieldCondition(key="user_id", match=MatchValue(value=user_id))
        ]

        if video_id:
            conditions.append(
                FieldCondition(key="video_id", match=MatchValue(value=video_id))
            )

        search_filter = Filter(must=conditions)

        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            query_filter=search_filter,
            limit=limit,
            with_payload=True
        )

        return results
    except Exception as e:
        print(f"Error searching Qdrant: {e}")
        raise

def delete_video_chunks(video_id: str):
    """Delete all chunks for a specific video"""
    try:
        client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=Filter(
                must=[FieldCondition(key="video_id", match=MatchValue(value=video_id))]
            )
        )
        print(f"Deleted chunks for video {video_id}")
    except Exception as e:
        print(f"Error deleting chunks: {e}")
        raise
