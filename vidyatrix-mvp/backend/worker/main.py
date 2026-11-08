import sys
import os
import time
import uuid
from faster_whisper import WhisperModel
import subprocess
from sqlalchemy.orm import Session

from database import SessionLocal, Base, engine
from models import Video, TranscriptChunk, VideoStatus
from embeddings import create_embeddings_batch
from qdrant_helper import init_collection, upsert_chunks, delete_video_chunks
from config import UPLOAD_DIR

def extract_audio(video_path: str) -> str:
    """Extract audio from video using FFmpeg"""
    audio_path = video_path.rsplit('.', 1)[0] + '.mp3'
    try:
        subprocess.run(
            ["ffmpeg", "-i", video_path, audio_path],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Audio extracted to: {audio_path}")
        return audio_path
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr}")
        raise

def transcribe_audio(audio_path: str) -> dict:
    """Transcribe audio using faster-whisper"""
    print("Loading Whisper model...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    print("Transcribing audio...")
    segments, info = model.transcribe(audio_path, word_timestamps=True)
    
    # Convert to format compatible with existing code
    result = {
        "duration": info.duration,
        "segments": []
    }
    
    for segment in segments:
        result["segments"].append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })
    
    print(f"Transcription complete. Duration: {info.duration:.2f}s")
    return result

def chunk_transcript(result: dict, chunk_size: int = 30, overlap: int = 5):
    """Chunk transcript by time intervals"""
    chunks = []
    duration = result.get("duration", 0)

    for start in range(0, int(duration), chunk_size - overlap):
        end = min(start + chunk_size, int(duration))

        # Find segments within this time range
        segment_texts = []
        for segment in result["segments"]:
            if segment["start"] >= start and segment["end"] <= end:
                segment_texts.append(segment["text"])

        if segment_texts:
            chunks.append({
                "start_time": float(start),
                "end_time": float(end),
                "text": " ".join(segment_texts)
            })

    return chunks

def process_video(video_id: str):
    """Process a single video: extract audio, transcribe, chunk, embed, store"""
    db = SessionLocal()
    try:
        # Get video
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            print(f"Video {video_id} not found")
            return

        print(f"Processing video: {video.title}")

        # Update status to processing
        video.status = VideoStatus.PROCESSING
        db.commit()

        # Extract audio
        audio_path = extract_audio(video.file_path)

        # Transcribe
        transcription = transcribe_audio(audio_path)

        # Update video duration
        video.duration = transcription.get("duration", 0)
        db.commit()

        # Chunk transcript
        chunks = chunk_transcript(transcription)
        print(f"Created {len(chunks)} chunks")

        # Generate embeddings
        texts = [c["text"] for c in chunks]
        print("Generating embeddings...")
        embeddings = create_embeddings_batch(texts)

        # Prepare chunks for Qdrant
        qdrant_chunks = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            qdrant_chunks.append({
                "id": str(uuid.uuid4()),  # Generate proper UUID for Qdrant
                "user_id": video.user_id,
                "video_id": str(video.id),
                "start_time": chunk["start_time"],
                "end_time": chunk["end_time"],
                "text": chunk["text"],
                "embedding": embedding
            })

        # Store in Qdrant
        print("Storing vectors in Qdrant...")
        upsert_chunks(qdrant_chunks)

        # Store chunks in database
        for chunk in chunks:
            db_chunk = TranscriptChunk(
                video_id=video.id,
                start_time=chunk["start_time"],
                end_time=chunk["end_time"],
                text=chunk["text"]
            )
            db.add(db_chunk)

        # Update status to completed
        video.status = VideoStatus.COMPLETED
        db.commit()

        print(f"Video {video_id} processed successfully")

        # Clean up audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)

    except Exception as e:
        print(f"Error processing video {video_id}: {e}")
        video.status = VideoStatus.FAILED
        video.error_message = str(e)
        db.commit()
    finally:
        db.close()

def main():
    """Main worker loop - polls for pending videos"""
    print("Starting video processing worker...")

    # Initialize Qdrant collection
    init_collection()

    while True:
        db = SessionLocal()
        try:
            # Get pending videos
            pending_videos = db.query(Video).filter(
                Video.status == VideoStatus.PENDING
            ).all()

            if pending_videos:
                print(f"Found {len(pending_videos)} pending videos")

                for video in pending_videos:
                    process_video(str(video.id))
            else:
                print("No pending videos. Waiting...")

        except Exception as e:
            print(f"Error in worker loop: {e}")
        finally:
            db.close()

        # Wait before next poll
        time.sleep(10)

if __name__ == "__main__":
    main()
