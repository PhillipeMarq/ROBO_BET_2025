import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

from telegram_utils import (
    analisar_jogos,
    analisar_jogo_individual,
    prever_resultado,
    sugestao_aposta
)

# ============ CONFIGURAÇÃO ============
TOKEN = "8124502590:AAHOzEYywnp6sNuEyDn9Lz4ZNyMIIfF8RiM"
CHAT_ID_ENVIO_DIARIO = 7178592047

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ============ COMANDOS ============
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Olá! Eu sou o robô de apostas esportivas.\n\n"
        "📊 Use os comandos abaixo:\n"
        "/analise Flamengo x Grêmio - para análise completa\n"
        "/prever Palmeiras x Vasco - para previsão com IA"
    )

def analise(update: Update, context: CallbackContext):
    if context.args:
        jogo = ' '.join(context.args)
        resposta = analisar_jogo_individual(jogo)
    else:
        resposta = "\n\n".join(analisar_jogos())
    resposta += "\n" + sugestao_aposta()
    update.message.reply_text(resposta)

def prever(update: Update, context: CallbackContext):
    if context.args:
        jogo = ' '.join(context.args)
        resposta = prever_resultado(jogo)
        update.message.reply_text(resposta)
    else:
        update.message.reply_text("❗ Use assim: /prever Flamengo x Grêmio")

def analise_diaria(context: CallbackContext):
    try:
        texto = "\n\n".join(analisar_jogos())
        texto += "\n" + sugestao_aposta()
        context.bot.send_message(chat_id=CHAT_ID_ENVIO_DIARIO, text=texto)
        logging.info("✅ Análise diária enviada com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao enviar análise diária: {e}")

# ============ MAIN ============
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("analise", analise))
    dp.add_handler(CommandHandler("prever", prever))

    # Agendador diário às 9h
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        analise_diaria,
        trigger='cron',
        hour=9,
        minute=0,
        args=[updater.bot]
    )
    scheduler.start()

    print("🤖 Bot iniciado com polling...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
