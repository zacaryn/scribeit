import os
import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI
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

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def transcribe_audio(self, audio_file_path: str) -> Dict[str, Any]:
        """Transcribe audio file using OpenAI's API."""
        self.logger.info(f"Transcribing audio file: {audio_file_path}")
        try:
            with open(audio_file_path, "rb") as audio_file:
                # Simplified API call for current OpenAI version
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
        except Exception as e:
            self.logger.error(f"Error transcribing audio: {e}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_summary(self, text: str, prompt: Optional[str] = None) -> str:
        """Generate a summary of the given text using OpenAI's API."""
        self.logger.info(f"Generating summary for text of length: {len(text)}")
        
        base_prompt = "Please summarize the following text, highlighting the key points and main ideas:"
        if prompt:
            instruction = prompt
        else:
            instruction = base_prompt
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes texts."},
                    {"role": "user", "content": f"{instruction}\n\n{text}"}
                ],
                temperature=0.5,
                max_tokens=500
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
        # This is a simple parsing implementation
        # Could be improved with more robust parsing logic
        
        sections = summary_text.split("\n\n")
        result = {
            "summary": "",
            "key_points": [],
            "action_items": []
        }
        
        current_section = None
        
        for section in sections:
            if "Summary" in section or "SUMMARY" in section:
                current_section = "summary"
                result["summary"] = section.replace("Summary:", "").replace("SUMMARY:", "").strip()
            elif "Key Points" in section or "KEY POINTS" in section:
                current_section = "key_points"
            elif "Action Items" in section or "ACTION ITEMS" in section:
                current_section = "action_items"
            elif current_section in ["key_points", "action_items"]:
                # Process bullet points
                for line in section.split("\n"):
                    line = line.strip()
                    if line.startswith("- ") or line.startswith("• "):
                        result[current_section].append(line.replace("- ", "").replace("• ", ""))
        
        return result 