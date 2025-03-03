from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import tempfile
import os
import logging
import yt_dlp
import subprocess
import time
import random
from pydantic import BaseModel, HttpUrl
import uuid

# Add pytube as a fallback
try:
    from pytube import YouTube
    PYTUBE_AVAILABLE = True
except ImportError:
    PYTUBE_AVAILABLE = False

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

# Request models
class YouTubeRequest(BaseModel):
    url: HttpUrl
    title: str = None

def download_with_pytube(url, output_dir):
    """
    Fallback method using pytube to download YouTube audio
    """
    if not PYTUBE_AVAILABLE:
        raise ImportError("pytube is not available")
        
    logger.info(f"Attempting download with pytube: {url}")
    
    try:
        # Create YouTube object
        yt = YouTube(url)
        
        # Get video info
        video_title = yt.title
        video_duration = yt.length
        
        logger.info(f"pytube found video: '{video_title}' ({video_duration} seconds)")
        
        # Check duration
        if video_duration > 10800:  # 3 hours
            raise ValueError(f"Video is too long ({video_duration} seconds)")
            
        # Get audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            raise ValueError("No audio stream found for this video")
            
        # Download audio to temp directory
        logger.info(f"Downloading audio stream with pytube...")
        output_file = audio_stream.download(output_path=output_dir)
        logger.info(f"pytube downloaded file to: {output_file}")
        
        # Convert to MP3 using FFmpeg if available
        mp3_file = os.path.join(output_dir, f"{uuid.uuid4()}.mp3")
        try:
            # Check if ffmpeg is available
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            
            # Convert to MP3
            cmd = [
                "ffmpeg", 
                "-i", output_file,
                "-vn",  # No video
                "-ar", "44100",  # Audio sampling rate
                "-ac", "2",  # Stereo
                "-b:a", "192k",  # Bitrate
                "-f", "mp3",  # Format
                mp3_file
            ]
            
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Remove original file
            os.remove(output_file)
            
            logger.info(f"Converted to MP3: {mp3_file}")
            output_file = mp3_file
            
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.warning("FFmpeg not available, using original audio format")
            # Rename the file to have .mp3 extension for consistency
            mp3_file = output_file + ".mp3"
            os.rename(output_file, mp3_file)
            output_file = mp3_file
            
        return {
            'title': video_title,
            'duration': video_duration,
            'file_path': output_file
        }
        
    except Exception as e:
        logger.error(f"pytube download failed: {str(e)}")
        raise ValueError(f"pytube download failed: {str(e)}")

# Helper to download YouTube audio
def download_youtube_audio(url, output_path):
    """
    Download audio from YouTube video with enhanced error handling
    and the latest workarounds for 403 errors
    """
    # Latest recommended workarounds for YouTube 403 errors
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,  # Show output for better debugging
        'verbose': True,  # Verbose output helps diagnose issues
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'no_warnings': False,
        'geo_bypass': True,
        'extractor_retries': 10,  # Increased retries
        'socket_timeout': 30,
        
        # New options to bypass restrictions
        'cookiefile': None,  # No cookies needed for most videos
        'skip_download': False,
        'overwrites': True,
        'noplaylist': True,
        
        # Using a mobile user agent helps avoid some restrictions
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E150',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Origin': 'https://www.youtube.com',
            'Referer': 'https://www.youtube.com/',
        }
    }
    
    # New approach - try multiple methods in sequence
    methods_to_try = [
        # Method 1: Default approach with mobile user agent
        dict(ydl_opts),
        
        # Method 2: Try with different format selection
        {**ydl_opts, 'format': 'worstaudio/worst'},
        
        # Method 3: Try with a desktop user agent
        {**ydl_opts, 'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Origin': 'https://www.youtube.com',
            'Referer': 'https://www.youtube.com/',
        }},
        
        # Method 4: Try with the embed URL format (often bypasses restrictions)
        {**ydl_opts, 'extract_flat': True}
    ]
    
    # First validate the URL and get basic info
    video_title = None
    video_duration = 0
    
    try:
        logger.info(f"Validating YouTube URL: {url}")
        
        # Try to get info using a simpler configuration
        with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            
            if not info_dict:
                logger.error("Failed to extract video information")
                raise ValueError("Could not extract video information. The video may be private or unavailable.")
                
            video_title = info_dict.get('title', 'Unknown Title')
            video_duration = info_dict.get('duration', 0)
            
            logger.info(f"Validated YouTube video: '{video_title}' ({video_duration} seconds)")
            
            # Check if video is too long
            if video_duration > 10800:  # 3 hours
                logger.warning(f"Video is too long: {video_duration} seconds")
                raise ValueError(f"Video is too long ({video_duration} seconds). Maximum allowed duration is 3 hours.")
    except Exception as e:
        logger.warning(f"Validation phase error: {e}")
        # Continue anyway, we might still be able to download with one of our methods
    
    # Try each method in sequence until one works
    last_error = None
    attempt_count = 0
    
    for method_opts in methods_to_try:
        attempt_count += 1
        logger.info(f"Attempting download method {attempt_count}/{len(methods_to_try)}")
        
        try:
            # Use different URL formats based on the attempt
            current_url = url
            if attempt_count == 4:
                # For the last attempt, try the embed URL format
                video_id = url.split("v=")[-1].split("&")[0] if "v=" in url else url.split("/")[-1]
                current_url = f"https://www.youtube.com/embed/{video_id}"
                logger.info(f"Trying embed URL format: {current_url}")
            
            with yt_dlp.YoutubeDL(method_opts) as ydl:
                logger.info(f"Downloading audio from YouTube: {current_url}")
                ydl.extract_info(current_url, download=True)
                
                # Look for the downloaded MP3 file
                audio_dir = os.path.dirname(output_path)
                for file in os.listdir(audio_dir):
                    if file.endswith('.mp3'):
                        downloaded_file = os.path.join(audio_dir, file)
                        logger.info(f"Successfully downloaded audio to: {downloaded_file}")
                        
                        # If we didn't get title/duration before, extract from filename
                        if not video_title:
                            video_title = os.path.splitext(file)[0]
                        
                        # Return info dict and downloaded file path
                        return {
                            'title': video_title,
                            'duration': video_duration,
                            'file_path': downloaded_file
                        }
                        
                # If we got here but no file was found, something went wrong
                logger.warning("Download seemed to succeed but no MP3 file was found")
                
        except Exception as e:
            last_error = e
            error_msg = str(e)
            logger.warning(f"Method {attempt_count} failed: {error_msg}")
            # Continue to the next method
    
    # If all yt-dlp methods failed, try pytube as a last resort
    if PYTUBE_AVAILABLE:
        logger.info("All yt-dlp methods failed, attempting pytube as fallback")
        try:
            output_dir = os.path.dirname(output_path)
            return download_with_pytube(url, output_dir)
        except Exception as e:
            logger.error(f"pytube fallback failed: {e}")
            last_error = e
            
    # If we get here, all methods failed
    logger.error(f"All download methods failed. Last error: {last_error}")
    
    # Provide helpful error based on the last error
    error_str = str(last_error) if last_error else "Unknown error"
    
    if "HTTP Error 403: Forbidden" in error_str:
        raise ValueError("YouTube has blocked this download. This may be due to content restrictions or YouTube's anti-bot measures. Please try a different video or try again later.")
    elif "Private video" in error_str:
        raise ValueError("This video is private. Please ensure the video is publicly accessible.")
    elif "Video unavailable" in error_str:
        raise ValueError("This video is unavailable. It may have been removed or region-restricted.")
    elif "This video is available for Premium users only" in error_str or "paywall" in error_str.lower():
        raise ValueError("This video is available for YouTube Premium users only and cannot be processed.")
    else:
        raise ValueError(f"Failed to download YouTube video: {error_str}")

# Helper to process YouTube video
def process_youtube_video(url, summary_id, db):
    """
    Process YouTube video, store results in database
    """
    temp_dir = None
    
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
        output_path = os.path.join(temp_dir, f"youtube_audio.%(ext)s")
        
        # Download YouTube audio
        video_info = download_youtube_audio(url, output_path)
        
        # Extract info from the result
        downloaded_file = video_info['file_path']
        video_title = video_info['title']
        video_duration = video_info['duration']
        
        # Update summary with video metadata
        summary.title = summary.title or video_title
        summary.duration_seconds = video_duration
        summary.minutes_charged = video_duration / 60 if video_duration else 0
        db.commit()
        
        # Upload to S3
        with open(downloaded_file, 'rb') as file:
            s3_key = s3_service.upload_file(
                file, 
                f"{video_title}.mp3", 
                summary.user_id
            )
        
        # Update summary with S3 key
        summary.s3_file_key = s3_key
        db.commit()
        
        # Transcribe file
        logger.info(f"Transcribing audio file: {downloaded_file}")
        transcription_result = openai_service.transcribe_audio(downloaded_file)
        transcription_text = transcription_result["text"]
        
        # Generate summary
        logger.info("Generating summary from transcription")
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
        if temp_dir and os.path.exists(temp_dir):
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except Exception as cleanup_error:
                logger.warning(f"Failed to clean up temp directory: {cleanup_error}")

@router.post("/process")
async def process_youtube(
    request: YouTubeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    # Use real user authentication
    current_user: User = Depends(get_current_user)
):
    """
    Process a YouTube video URL
    """
    try:
        # Create a new summary record
        new_summary = Summary(
            user_id=current_user.id,
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