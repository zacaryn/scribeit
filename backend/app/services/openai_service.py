import os
import logging
import tempfile
import math
import io
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
from openai import OpenAI, APIStatusError
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        # Simple initialization without proxy parameters
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.logger = logging.getLogger(__name__)
        self.MAX_FILE_SIZE = 24 * 1024 * 1024  # 24MB to be safe (OpenAI limit is 25MB)

    def _get_file_size(self, file_path: str) -> int:
        """Get file size in bytes"""
        return os.path.getsize(file_path)

    def _is_audio_format_supported(self, file_path: str) -> bool:
        """Check if the file format is supported by OpenAI's API"""
        supported_extensions = ['.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm']
        return Path(file_path).suffix.lower() in supported_extensions

    def _check_ffmpeg_available(self) -> bool:
        """Check if FFmpeg is available in the system PATH"""
        try:
            subprocess.run(
                ["ffmpeg", "-version"], 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def _get_audio_duration(self, file_path: str) -> float:
        """Get audio/video file duration in seconds using FFmpeg"""
        try:
            # Use FFprobe to get duration
            cmd = [
                "ffprobe", 
                "-v", "error", 
                "-show_entries", "format=duration", 
                "-of", "default=noprint_wrappers=1:nokey=1", 
                file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            duration = float(result.stdout.strip())
            return duration
        except (subprocess.SubprocessError, ValueError) as e:
            self.logger.warning(f"Failed to get duration with FFmpeg: {e}")
            return 0.0

    def _split_audio_file(self, file_path: str, segment_length_seconds: int = 300) -> List[str]:
        """
        Split audio/video file into smaller segments using FFmpeg
        Args:
            file_path: Path to the audio/video file
            segment_length_seconds: Length of each segment in seconds (default: 5 minutes)
        Returns:
            List of paths to the segment files
        """
        self.logger.info(f"Splitting audio/video file using FFmpeg: {file_path}")
        
        # Check if FFmpeg is available
        if not self._check_ffmpeg_available():
            raise RuntimeError("FFmpeg is required but not found in PATH")
        
        # Create temp directory for segments
        temp_dir = tempfile.mkdtemp()
        file_extension = Path(file_path).suffix
        output_pattern = os.path.join(temp_dir, f"segment_%03d{file_extension}")
        
        try:
            # Execute FFmpeg to split the file into segments
            cmd = [
                "ffmpeg", 
                "-i", file_path,
                "-f", "segment", 
                "-segment_time", str(segment_length_seconds),
                "-c", "copy",  # Copy codec (no re-encoding)
                "-reset_timestamps", "1",  # Reset timestamps for each segment
                "-map", "0",  # Map all streams
                "-loglevel", "warning",
                output_pattern
            ]
            
            self.logger.info(f"Running FFmpeg command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.logger.debug(f"FFmpeg output: {result.stdout}")
            
            # Get list of generated segment files
            segment_files = sorted([
                os.path.join(temp_dir, f) 
                for f in os.listdir(temp_dir)
                if os.path.isfile(os.path.join(temp_dir, f))
            ])
            
            if not segment_files:
                raise RuntimeError("FFmpeg did not generate any segment files")
                
            self.logger.info(f"Created {len(segment_files)} segments from audio/video file")
            return segment_files
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"FFmpeg error: {e.stderr}")
            raise RuntimeError(f"Failed to split audio/video file: {e.stderr}")
        except Exception as e:
            self.logger.error(f"Error splitting file: {str(e)}")
            raise

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=2, max=4))
    def transcribe_audio(self, audio_file_path: str) -> Dict[str, Any]:
        """Transcribe audio file using OpenAI's API."""
        self.logger.info(f"Transcribing audio file: {audio_file_path}")
        
        # Check if format is supported
        if not self._is_audio_format_supported(audio_file_path):
            error_msg = f"Unsupported file format: {Path(audio_file_path).suffix}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Check file size
        file_size = self._get_file_size(audio_file_path)
        self.logger.info(f"Audio file size: {file_size / (1024 * 1024):.2f} MB")
        
        # First attempt: Try transcribing the entire file if it's within or close to the size limit
        if file_size <= self.MAX_FILE_SIZE * 1.1:  # Allow 10% margin
            try:
                self.logger.info("Attempting to transcribe the entire file")
                with open(audio_file_path, "rb") as audio_file:
                    response = self.client.audio.transcriptions.create(
                        file=audio_file,
                        model="whisper-1"
                    )
                    
                    # Handle response based on its structure
                    if hasattr(response, 'text'):
                        text = response.text
                        segments = getattr(response, 'segments', [])
                    elif isinstance(response, dict):
                        text = response.get('text', '')
                        segments = response.get('segments', [])
                    else:
                        text = str(response)
                        segments = []
                    
                    return {"text": text, "segments": segments}
            except APIStatusError as e:
                # If the file is too large, we'll get a 413 error
                self.logger.warning(f"Failed to transcribe entire file: {e}")
                # Continue to the splitting approach below
            except Exception as e:
                self.logger.error(f"Unexpected error transcribing audio: {e}")
                raise
        
        # If we're here, either the file is too large or the direct transcription failed
        # Split the file using FFmpeg and transcribe each segment
        self.logger.info("File is too large for OpenAI API, using FFmpeg to split into chunks")
        
        try:
            # Get audio duration for progress reporting
            audio_duration = self._get_audio_duration(audio_file_path)
            self.logger.info(f"Audio duration: {audio_duration:.2f} seconds")
            
            # Define segment length in seconds (matching the default in _split_audio_file)
            segment_length_seconds = 300  # 5 minutes per segment
            
            # Split the file using FFmpeg
            segment_files = self._split_audio_file(audio_file_path, segment_length_seconds)
            
            # Transcribe each segment
            full_text = ""
            all_segments = []
            total_segments = len(segment_files)
            
            for i, segment_file in enumerate(segment_files):
                segment_size = self._get_file_size(segment_file)
                segment_number = i + 1
                approx_start_time = i * segment_length_seconds  # Approximate start time in seconds
                
                # Format timestamp as HH:MM:SS
                start_time_formatted = self._format_timestamp(approx_start_time)
                
                self.logger.info(f"Transcribing segment {segment_number}/{total_segments} ({segment_size / (1024 * 1024):.2f} MB)")
                
                # Add segment heading with timestamp
                if i > 0:
                    full_text += f"\n\n"
                
                # Skip segments that are still too large
                if segment_size > self.MAX_FILE_SIZE:
                    self.logger.warning(f"Segment {segment_number} is still too large ({segment_size / (1024 * 1024):.2f} MB), skipping")
                    full_text += f"[Segment {segment_number} at {start_time_formatted} skipped due to size limitations]"
                    continue
                
                try:
                    with open(segment_file, "rb") as audio_file:
                        response = self.client.audio.transcriptions.create(
                            file=audio_file,
                            model="whisper-1"
                        )
                        
                        # Handle response
                        if hasattr(response, 'text'):
                            text = response.text
                            segments = getattr(response, 'segments', [])
                        elif isinstance(response, dict):
                            text = response.get('text', '')
                            segments = response.get('segments', [])
                        else:
                            text = str(response)
                            segments = []
                        
                        # Update segment timestamps if available
                        if segments:
                            for segment in segments:
                                if hasattr(segment, 'start') and segment.start is not None:
                                    # Adjust segment timestamps to account for position in the full audio
                                    segment.start += approx_start_time
                                if hasattr(segment, 'end') and segment.end is not None:
                                    segment.end += approx_start_time
                        
                        # Add formatted text from this segment
                        cleaned_text = text.strip()
                        if cleaned_text:
                            full_text += cleaned_text
                        
                        # Add segments to the collection
                        all_segments.extend(segments)
                        
                except Exception as e:
                    self.logger.error(f"Error transcribing segment {segment_number}: {e}")
                    full_text += f"[Error transcribing segment {segment_number} at {start_time_formatted}]"
            
            # Final text processing - clean up potential artifacts from combining segments
            processed_text = self._process_combined_transcript(full_text)
            
            # Clean up temporary files
            for segment_file in segment_files:
                try:
                    os.remove(segment_file)
                except Exception as e:
                    self.logger.warning(f"Failed to remove temp file {segment_file}: {e}")
            
            # Clean up temp directory
            try:
                os.rmdir(os.path.dirname(segment_files[0]))
            except Exception as e:
                self.logger.warning(f"Failed to remove temp directory: {e}")
                
            if not processed_text.strip():
                raise ValueError("Failed to transcribe any segments of the file")
                
            return {"text": processed_text.strip(), "segments": all_segments}
            
        except Exception as e:
            self.logger.error(f"Error processing file with FFmpeg: {e}")
            raise ValueError(f"Failed to process large file: {str(e)}")

    def _format_timestamp(self, seconds: float) -> str:
        """Format seconds as HH:MM:SS"""
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def _process_combined_transcript(self, text: str) -> str:
        """
        Process the combined transcript text to improve readability
        - Fix common artifacts from segment combination
        - Add proper paragraph breaks
        - Clean up punctuation and spacing
        """
        if not text:
            return ""
        
        # Replace multiple newlines with double newlines (for paragraph breaks)
        processed = '\n\n'.join(p.strip() for p in text.split('\n') if p.strip())
        
        # Fix common segment boundary issues
        # 1. Fix sentences that got cut off between segments (lowercase after period)
        processed = processed.replace('. a', '. A')
        processed = processed.replace('. t', '. T')
        processed = processed.replace('. i', '. I')
        
        # 2. Fix missing spaces after punctuation
        for punct in ['.', ',', '!', '?', ';', ':']:
            processed = processed.replace(f"{punct}", f"{punct} ")
            # Clean up any double spaces this might create
            processed = processed.replace("  ", " ")
        
        # 3. Fix double punctuation that might occur at segment boundaries
        for punct in ['.', ',', '!', '?']:
            processed = processed.replace(f"{punct}{punct}", f"{punct}")
        
        # 4. Ensure proper capitalization after sentence endings
        for end_punct in ['. ', '! ', '? ']:
            segments = processed.split(end_punct)
            for i in range(1, len(segments)):
                if segments[i] and segments[i][0].islower():
                    segments[i] = segments[i][0].upper() + segments[i][1:]
            processed = end_punct.join(segments)
        
        return processed.strip()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_summary(self, text: str, prompt: Optional[str] = None) -> str:
        """Generate a summary of the given text using OpenAI's API."""
        self.logger.info(f"Generating summary for text of length: {len(text)}")
        
        # Define a more structured prompt for our use case
        base_prompt = """
You are an expert summarizer for Scribe It, a service that condenses videos into comprehensive summaries.

Please analyze the following transcript and generate a structured summary with these components:

1. OVERVIEW: A concise 2-3 paragraph summary of the main content and context of the discussion.

2. KEY POINTS: A bullet-point list of the 5-8 most important insights, facts, or topics covered.

3. ACTION ITEMS: A bullet-point list of specific tasks, follow-ups, or commitments mentioned by participants.

4. NOTABLE QUOTES: 2-3 significant or representative quotes from the transcript (with attribution if possible).

Format your response with clear headings for each section.
"""
        if prompt:
            instruction = prompt
        else:
            instruction = base_prompt
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Using more advanced model for better summarization
                messages=[
                    {"role": "system", "content": "You are an expert summarizer that extracts key information from transcripts and produces clear, structured summaries."},
                    {"role": "user", "content": f"{instruction}\n\n{text}"}
                ],
                temperature=0.3,  # Lower temperature for more focused output
                max_tokens=1000   # Increased token limit for more comprehensive summaries
            )
            
            # Access the message content using the current response structure
            summary = response.choices[0].message.content
            return summary
        except Exception as e:
            self.logger.error(f"Error generating summary: {e}")
            raise
            
    def parse_summary_response(self, summary_text):
        """
        Parse the summary response into structured data
        """
        # Enhanced parsing implementation for the new structured format
        result = {
            "summary": "",
            "key_points": [],
            "action_items": [],
            "notable_quotes": []
        }
        
        # Split by headers (both uppercase and regular case)
        current_section = None
        lines = summary_text.split("\n")
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Check for section headers
            lowered = line.lower()
            if "overview" in lowered or "summary" in lowered:
                current_section = "summary"
                continue
            elif "key points" in lowered:
                current_section = "key_points"
                continue
            elif "action items" in lowered:
                current_section = "action_items"
                continue
            elif "notable quotes" in lowered:
                current_section = "notable_quotes"
                continue
            
            # Process content based on current section
            if current_section == "summary":
                if result["summary"]:
                    result["summary"] += " " + line
                else:
                    result["summary"] = line
            elif current_section in ["key_points", "action_items", "notable_quotes"]:
                # Check if the line is a bullet point
                if line.startswith("- ") or line.startswith("• ") or line.startswith("* "):
                    clean_line = line.replace("- ", "").replace("• ", "").replace("* ", "")
                    result[current_section].append(clean_line)
                # Handle numbered lists
                elif line[0].isdigit() and len(line) > 2 and line[1:3] in [". ", ") ", "- "]:
                    clean_line = line[3:].strip()
                    result[current_section].append(clean_line)
                # If not a bullet but we're in a bullet point section, it might be a continuation
                elif current_section in ["key_points", "action_items", "notable_quotes"] and result[current_section]:
                    # Append to the last bullet point as a continuation
                    result[current_section][-1] += " " + line
        
        return result 