from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
import tempfile
import os
import logging
# Removing pydub import since it's not compatible with Python 3.13
# from pydub import AudioSegment
from typing import Optional
import shutil

from ...db.database import get_db
from ...models.user import User
from ...models.summary import Summary
from ...services.s3_service import S3Service
from ...services.openai_service import OpenAIService
# Enable authentication
from ...core.auth import get_current_user

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
s3_service = S3Service()
openai_service = OpenAIService()

# Helper to process audio/video files
def process_media_file(file_path, summary_id, db):
    """
    Process uploaded media file, store results in database
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
        
        # Transcribe file
        transcription_result = openai_service.transcribe_audio(file_path)
        transcription_text = transcription_result["text"]
        
        # Generate summary
        summary_response = openai_service.generate_summary(transcription_text)
        parsed_summary = openai_service.parse_summary_response(summary_response)
        
        # Update summary in database
        summary.transcription = transcription_text
        summary.summary_text = parsed_summary["summary"]
        summary.key_points = parsed_summary["key_points"]
        summary.action_items = parsed_summary["action_items"]
        summary.notable_quotes = parsed_summary.get("notable_quotes", [])
        summary.status = "completed"
        
        # Commit changes
        db.commit()
        
        logger.info(f"Successfully processed summary {summary_id}")
        
    except Exception as e:
        logger.error(f"Error processing media file: {str(e)}")
        
        # Update summary with error
        summary = db.query(Summary).filter(Summary.id == summary_id).first()
        if summary:
            summary.status = "failed"
            summary.error_message = str(e)
            db.commit()
    finally:
        # Clean up temp file
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/upload", response_model=dict)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    # Use real user authentication
    current_user: User = Depends(get_current_user)
):
    """
    Upload and process an audio/video file
    """
    try:
        # Validate file extension
        allowed_extensions = {"mp3", "mp4", "wav", "m4a", "webm"}
        file_extension = file.filename.split(".")[-1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File extension {file_extension} not allowed. Allowed extensions: {allowed_extensions}"
            )
        
        # Create a new summary record
        new_summary = Summary(
            user_id=current_user.id,
            title=title or file.filename,
            source_type="file_upload",
            original_filename=file.filename,
            status="pending"
        )
        
        db.add(new_summary)
        db.commit()
        db.refresh(new_summary)
        
        # Save file to S3
        s3_key = s3_service.upload_file(file.file, file.filename, current_user.id)
        
        # Update summary with S3 key
        new_summary.s3_file_key = s3_key
        db.commit()
        
        # Create temp file
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, file.filename)
        
        # Reset file pointer and save to temp file
        file.file.seek(0)
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process file in background
        background_tasks.add_task(
            process_media_file,
            temp_file_path,
            new_summary.id,
            db
        )
        
        return {
            "message": "File uploaded successfully, processing started",
            "summary_id": new_summary.id
        }
        
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{summary_id}")
async def get_status(
    summary_id: str,
    db: Session = Depends(get_db),
    # Use real user authentication
    current_user: User = Depends(get_current_user)
):
    """
    Get processing status for a summary
    """
    summary = db.query(Summary).filter(Summary.id == summary_id).first()
    
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    
    # Check if the summary belongs to the current user
    if summary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this summary")
    
    return {
        "summary_id": summary.id,
        "status": summary.status,
        "title": summary.title,
        "created_at": summary.created_at,
        "error_message": summary.error_message
    }

@router.get("/result/{summary_id}")
async def get_result(
    summary_id: str,
    db: Session = Depends(get_db),
    # Use real user authentication
    current_user: User = Depends(get_current_user)
):
    """
    Get processing result for a summary
    """
    summary = db.query(Summary).filter(Summary.id == summary_id).first()
    
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    
    # Check if the summary belongs to the current user
    if summary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this summary")
    
    if summary.status != "completed":
        return {
            "summary_id": summary.id,
            "status": summary.status,
            "title": summary.title,
            "created_at": summary.created_at,
            "error_message": summary.error_message
        }
    
    return {
        "summary_id": summary.id,
        "status": summary.status,
        "title": summary.title,
        "created_at": summary.created_at,
        "transcription": summary.transcription,
        "summary": summary.summary_text,
        "key_points": summary.key_points,
        "action_items": summary.action_items
    } 