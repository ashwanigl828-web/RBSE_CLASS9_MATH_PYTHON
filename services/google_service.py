import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config import Config
from utils.logger import setup_logger

logger = setup_logger()

class GoogleDriveDB:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds_file = 'credentials.json'
        self.service = None
        self.sheet_id = Config.GOOGLE_SHEET_ID
        
    def authenticate(self):
        if not os.path.exists(self.creds_file):
            logger.warning("credentials.json not found. Database features disabled.")
            return False
            
        try:
            creds = Credentials.from_service_account_file(self.creds_file, scopes=self.scopes)
            self.service = build('sheets', 'v4', credentials=creds)
            return True
        except Exception as e:
            logger.error(f"Google API Auth Error: {e}")
            return False

    def get_current_topic(self):
        if not self.service or not self.sheet_id:
            return "अध्याय 1: संख्या पद्धति" # Fallback
            
        try:
            sheet = self.service.spreadsheets()
            # Assuming 'Topics' sheet, cell A1 has the current topic
            result = sheet.values().get(spreadsheetId=self.sheet_id, range='Topics!A1').execute()
            values = result.get('values', [])
            if values:
                return values[0][0]
        except Exception as e:
            logger.error(f"Error reading topic: {e}")
        return "अध्याय 1: संख्या पद्धति"
        
    def save_quiz_result(self, name, score):
        if not self.service or not self.sheet_id:
            return False
            
        try:
            sheet = self.service.spreadsheets()
            body = {'values': [[name, score]]}
            sheet.values().append(
                spreadsheetId=self.sheet_id,
                range='Results!A:B',
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            return True
        except Exception as e:
            logger.error(f"Error saving result: {e}")
            return False

google_db = GoogleDriveDB()
