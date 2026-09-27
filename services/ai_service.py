import json
from groq import Groq
from config import Config
from utils.logger import setup_logger
from utils.prompts import NOTES_PROMPT, QUIZ_PROMPT

logger = setup_logger()

class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def generate_notes_html(self, topic):
        if not self.client:
            logger.error("Groq API key not configured")
            return None
            
        try:
            logger.info(f"Generating notes for: {topic}")
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": NOTES_PROMPT.format(topic=topic)}
                ],
                model="llama-3.1-70b-versatile",
                temperature=0.5,
                max_tokens=2048
            )
            html_content = chat_completion.choices[0].message.content
            # Clean up potential markdown formatting from AI output
            html_content = html_content.replace('```html', '').replace('```', '').strip()
            return html_content
        except Exception as e:
            logger.error(f"Error generating notes: {e}")
            return None

    def generate_quiz_json(self, topic):
        if not self.client:
            return None
            
        try:
            logger.info(f"Generating quiz for: {topic}")
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": QUIZ_PROMPT.format(topic=topic)}
                ],
                model="llama-3.1-70b-versatile",
                temperature=0.3,
                max_tokens=1500
            )
            raw_text = chat_completion.choices[0].message.content
            raw_text = raw_text.replace('```json', '').replace('```', '').strip()
            
            # Find JSON array limits in case AI adds extra text
            start_idx = raw_text.find('[')
            end_idx = raw_text.rfind(']') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = raw_text[start_idx:end_idx]
                return json.loads(json_str)
            return None
        except Exception as e:
            logger.error(f"Error generating quiz: {e}")
            return None

ai_service = AIService()
