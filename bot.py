import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import Config
from utils.logger import setup_logger
from utils.html_parser import html_to_telegraph_nodes
from services.ai_service import ai_service
from services.telegraph_api import telegraph_service
from services.google_service import google_db

logger = setup_logger()

# Authenticate Google DB
google_db.authenticate()

async def send_to_admin(context: ContextTypes.DEFAULT_TYPE, message: str):
    if Config.TELEGRAM_ADMIN_CHAT_ID:
        try:
            await context.bot.send_message(chat_id=Config.TELEGRAM_ADMIN_CHAT_ID, text=message)
        except Exception as e:
            logger.error(f"Failed to send to admin: {e}")

# ================= Scheduled Jobs =================

async def job_morning_notes(context: ContextTypes.DEFAULT_TYPE):
    """Runs at 8:00 AM"""
    logger.info("Running Morning Notes Job")
    topic = google_db.get_current_topic()
    
    # 1. Generate Notes (AI)
    html_notes = ai_service.generate_notes_html(topic)
    if not html_notes:
        await send_to_admin(context, "⚠️ 8 AM Alert: Failed to generate notes via Groq. (Will retry in 5 mins if configured)")
        return
        
    # 2. Convert to Telegraph format
    nodes = html_to_telegraph_nodes(html_notes)
    
    # 3. Publish to Telegraph (graph.org)
    title = f"{Config.CLASS_NAME} - {topic}"
    url = telegraph_service.create_page(title, nodes)
    
    if url:
        msg = f"📚 **आज का गणित का पाठ ({Config.CLASS_NAME})**\n\n📝 टॉपिक: {topic}\n🔗 नोट्स यहाँ पढ़ें: {url}\n\n(इसे कॉपी करके WhatsApp ग्रुप में भेज दें)"
        await send_to_admin(context, msg)
    else:
        await send_to_admin(context, "⚠️ 8 AM Alert: Failed to publish notes to graph.org")

async def job_evening_quiz(context: ContextTypes.DEFAULT_TYPE):
    """Runs at 5:00 PM"""
    logger.info("Running Evening Quiz Job")
    topic = google_db.get_current_topic()
    
    quiz_json = ai_service.generate_quiz_json(topic)
    if not quiz_json:
        await send_to_admin(context, "⚠️ 5 PM Alert: Failed to generate quiz.")
        return
        
    # In a fully integrated version, we'd use Google Forms API here.
    # For now, we just output the quiz JSON to Telegraph as a readable test link, 
    # OR we tell the admin the questions so they can paste them.
    
    # Let's create a temporary quiz page
    content_nodes = [{"tag": "h3", "children": ["आज का क्विज़ (प्रश्नोत्तरी)"]}]
    for i, q in enumerate(quiz_json):
        content_nodes.append({"tag": "p", "children": [f"Q{i+1}: {q['question']}"]})
        for j, opt in enumerate(q['options']):
            content_nodes.append({"tag": "p", "children": [f" - {opt}"]})
            
    url = telegraph_service.create_page(f"Quiz - {topic}", content_nodes)
    
    msg = f"🧠 **शाम का क्विज़ ({Config.CLASS_NAME})**\n\n📝 टॉपिक: {topic}\n🔗 क्विज़ के प्रश्न यहाँ देखें: {url}\n\n(Google Forms लिंक के लिए Credentials.json सेट करें)"
    await send_to_admin(context, msg)

# ================= Telegram Commands =================

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("नमस्ते! मैं RBSE Class 9 Math Bot हूँ। मैं अपने आप सुबह 8 बजे और शाम 5 बजे काम करूँगा।")

async def force_notes_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("नोट्स जनरेट कर रहा हूँ... कृपया प्रतीक्षा करें (10-20 सेकंड)।")
    await job_morning_notes(context)

# ================= Main Entry Point =================

def main():
    if not Config.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found!")
        return

    app = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("notes", force_notes_cmd))

    # Scheduler setup
    scheduler = AsyncIOScheduler(timezone=Config.TIMEZONE)
    scheduler.add_job(job_morning_notes, CronTrigger(hour=8, minute=0), args=[app])
    scheduler.add_job(job_evening_quiz, CronTrigger(hour=17, minute=0), args=[app])
    scheduler.start()

    logger.info("Bot started successfully. Waiting for tasks...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
