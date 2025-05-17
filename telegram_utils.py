
import os
import telegram

def send_message(text):
    bot = telegram.Bot(token=os.getenv("8124502590:AAHOzEYywnp6sNuEyDn9Lz4ZNyMIIfF8RiM"))
    chat_id = os.getenv("7178592047")
    if chat_id:
        bot.send_message(chat_id=chat_id, text=text)
