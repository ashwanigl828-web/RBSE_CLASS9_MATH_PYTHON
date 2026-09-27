import os
import threading
from flask import Flask
from bot import main as start_bot
from utils.logger import setup_logger

logger = setup_logger()

# Initialize Flask app (Required for Render Web Service to bind to a port)
app = Flask(__name__)

@app.route('/')
def home():
    return "RBSE Class 9 Math Bot is running!"

@app.route('/ping')
def ping():
    # This endpoint will be used by cron-job.org to keep the Render server awake
    return "Pong! Server is awake."

# Start the Telegram Bot in a separate background thread
# This will run when gunicorn loads the app
logger.info("Starting Telegram Bot thread...")
bot_thread = threading.Thread(target=start_bot)
bot_thread.daemon = True
bot_thread.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
