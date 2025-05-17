
import os
import telegram

def send_message(text):
    bot = telegram.Bot(token=os.getenv("BOT_TOKEN"))
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if chat_id:
        bot.send_message(chat_id=chat_id, text=text)
