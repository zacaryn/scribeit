import os
import openai
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

class OpenAIService:
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def transcribe_audio(self, file_path):
        """
        Transcribe audio using OpenAI Whisper API
        """
        try:
            logger.info(f"Transcribing audio file: {file_path}")
            
            with open(file_path, "rb") as audio_file:
                response = client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-1",
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )
            
            return {
                "text": response.text,
                "segments": response.segments
            }
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate_summary(self, transcription):
        """
        Generate summary from transcription using OpenAI GPT model
        """
        try:
            logger.info("Generating summary from transcription")
            
            prompt = f"""
            Please analyze the following meeting transcription and provide:
            1. A concise summary (max 500 words)
            2. Key points (bullet points)
            3. Action items (if any, in bullet points)
            
            Transcription:
            {transcription}
            """
            
            response = client.chat.completions.create(
                model="gpt-4",  # Or gpt-3.5-turbo for cost savings
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts accurately and concisely."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
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