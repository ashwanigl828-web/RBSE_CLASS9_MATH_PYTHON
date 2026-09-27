import requests
import json
from utils.logger import setup_logger

logger = setup_logger()

# Using graph.org because telegra.ph is blocked by some Indian ISPs
BASE_URL = 'https://api.graph.org'

class TelegraphService:
    def __init__(self):
        self.access_token = None

    def create_account(self):
        if self.access_token:
            return self.access_token
            
        try:
            logger.info("Creating Telegraph (graph.org) account...")
            res = requests.post(f"{BASE_URL}/createAccount", json={
                "short_name": "MathBot",
                "author_name": "RBSE Class 9 Math"
            })
            data = res.json()
            if data.get("ok"):
                self.access_token = data["result"]["access_token"]
                return self.access_token
            else:
                logger.error(f"Failed to create Telegraph account: {data}")
                return None
        except Exception as e:
            logger.error(f"Error creating Telegraph account: {e}")
            return None

    def create_page(self, title, content_nodes):
        """
        Creates a Telegraph page.
        content_nodes should be a list of DOM nodes.
        """
        token = self.create_account()
        if not token:
            return None
            
        try:
            logger.info(f"Creating Telegraph page: {title}")
            res = requests.post(f"{BASE_URL}/createPage", json={
                "access_token": token,
                "title": title,
                "author_name": "RBSE Class 9 Math",
                "content": content_nodes,
                "return_content": False
            })
            data = res.json()
            if data.get("ok"):
                return data["result"]["url"]
            else:
                logger.error(f"Failed to create page: {data}")
                return None
        except Exception as e:
            logger.error(f"Error creating Telegraph page: {e}")
            return None

telegraph_service = TelegraphService()
