from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import tempfile
import os
import logging
import yt_dlp
from pydantic import BaseModel, HttpUrl
import uuid

from ...db.database import get_db
from ...models.user import User
from ...models.summary import Summary
from ...services.s3_service import S3Service
from ...services.openai_service import OpenAIService
# In a real app you would have authentication
# from ...core.auth import get_current_user

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
s3_service = S3Service()
openai_service = OpenAIService()

# Request models
class YouTubeRequest(BaseModel):
    url: HttpUrl
    title: str = None

# Helper to download YouTube audio
def download_youtube_audio(url, output_path):
    """
    Download audio from YouTube video
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            return info
        except Exception as e:
            logger.error(f"Error downloading YouTube audio: {str(e)}")
            raise

# Helper to process YouTube video
def process_youtube_video(url, summary_id, db):
    """
    Process YouTube video, store results in database
    """
    try:
        # Get summary from database
        summary = db.query(Summary).filter(Summary.id == summary_id).first()
        if not summary:
            logger.error(f"Summary not found: {summary_id}")
            return
        
        # Update status
        summary.status = "processing"
        db.commit()
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, f"{uuid.uuid4()}.%(ext)s")
        
        # Download YouTube audio
        video_info = download_youtube_audio(url, output_path)
        
        # Get downloaded file path (with correct extension)
        downloaded_file = os.path.join(temp_dir, f"{uuid.uuid4()}.mp3")
        
        # Update summary with video metadata
        summary.duration_seconds = video_info.get('duration')
        summary.minutes_charged = summary.duration_seconds / 60 if summary.duration_seconds else 0
        db.commit()
        
        # Upload to S3
        with open(downloaded_file, 'rb') as file:
            s3_key = s3_service.upload_file(
                file, 
                f"{video_info.get('title', 'youtube_video')}.mp3", 
                summary.user_id
            )
        
        # Update summary with S3 key
        summary.s3_file_key = s3_key
        db.commit()
        
        # Transcribe file
        transcription_result = openai_service.transcribe_audio(downloaded_file)
        transcription_text = transcription_result["text"]
        
        # Generate summary
        summary_response = openai_service.generate_summary(transcription_text)
        parsed_summary = openai_service.parse_summary_response(summary_response)
        
        # Update summary in database
        summary.transcription = transcription_text
        summary.summary_text = parsed_summary["summary"]
        summary.key_points = parsed_summary["key_points"]
        summary.action_items = parsed_summary["action_items"]
        summary.status = "completed"
        
        # Commit changes
        db.commit()
        
        logger.info(f"Successfully processed YouTube video {summary_id}")
        
    except Exception as e:
        logger.error(f"Error processing YouTube video: {str(e)}")
        
        # Update summary with error
        summary = db.query(Summary).filter(Summary.id == summary_id).first()
        if summary:
            summary.status = "failed"
            summary.error_message = str(e)
            db.commit()
    finally:
        # Clean up temp directory
        if os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)

@router.post("/process")
async def process_youtube(
    request: YouTubeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    # In a real app, you would uncomment this:
    # current_user: User = Depends(get_current_user)
):
    """
    Process a YouTube video URL
    """
    # For demo purposes, we're using a mock user
    # In a real app, you would use the authenticated user
    mock_user_id = "mock-user-123"
    
    try:
        # Create a new summary record
        new_summary = Summary(
            user_id=mock_user_id,
            title=request.title or "YouTube Video",
            source_type="youtube",
            source_url=str(request.url),
            status="pending"
        )
        
        db.add(new_summary)
        db.commit()
        db.refresh(new_summary)
        
        # Process YouTube video in background
        background_tasks.add_task(
            process_youtube_video,
            str(request.url),
            new_summary.id,
            db
        )
        
        return {
            "message": "YouTube video processing started",
            "summary_id": new_summary.id
        }
        
    except Exception as e:
        logger.error(f"Error processing YouTube video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 