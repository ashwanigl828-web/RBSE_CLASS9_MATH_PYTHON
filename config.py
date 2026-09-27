import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_ADMIN_CHAT_ID = os.environ.get('TELEGRAM_ADMIN_CHAT_ID', '')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    
    # Times are in IST (Render uses UTC by default, so we might need to set TZ=Asia/Kolkata in Render)
    # But APScheduler allows setting timezone easily.
    TIMEZONE = 'Asia/Kolkata'
    
    # Google Sheets IDs (To be filled by user)
    GOOGLE_SHEET_ID = os.environ.get('GOOGLE_SHEET_ID', '')
    
    # Subject Details
    SUBJECT = 'Mathematics (RBSE)'
    CLASS_NAME = 'Class 9'
