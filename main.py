from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import logging
import os

# ======================= CONFIGURAÇÕES =======================

TOKEN = "8124502590:AAHOzEYywnp6sNuEyDn9Lz4ZNyMIIfF8RiM"
WEBHOOK_URL = "https://sinais-ia.onrender.com/webhook"

# ======================= INICIALIZAÇÃO =======================

app = Flask(__name__)
bot = Bot(token=TOKEN)

# Dispatcher responsável pelos comandos
dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

# ======================= HANDLERS DE COMANDO =======================

def start(update, context):
    update.message.reply_text("Olá! Eu sou o robô de apostas esportivas. Use /analise para receber uma análise!")

def analise(update, context):
    update.message.reply_text("🔎 Analisando jogos... (em breve trarei as estatísticas!)")

# ======================= REGISTRO DOS COMANDOS =======================

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("analise", analise))

# ======================= ROTA DO WEBHOOK =======================

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return 'ok'

# ======================= ROTA PRINCIPAL =======================

@app.route('/', methods=['GET'])
def index():
    return 'Bot está ativo!'

# ======================= CONFIGURAÇÃO DO WEBHOOK =======================

def set_webhook():
    success = bot.set_webhook(url=WEBHOOK_URL)
    if success:
        print("✅ Webhook configurado com sucesso!")
    else:
        print("❌ Falha ao configurar o webhook.")

# ======================= MAIN =======================

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    set_webhook()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
