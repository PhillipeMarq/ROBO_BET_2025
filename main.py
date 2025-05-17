import logging
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from analise_jogos import analisar_jogos_hoje, analisar_jogo_especifico
from previsor_ia import prever_resultado

# ============ CONFIGURAÇÃO ============
TOKEN = "8124502590:AAHOzEYywnp6sNuEyDn9Lz4ZNyMIIfF8RiM"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ============ COMANDOS ============
def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Olá! Eu sou o robô de apostas esportivas.\n\nUse:\n/analise Flamengo x Grêmio\n/prever Palmeiras x Vasco")

def analise(update: Update, context: CallbackContext):
    if context.args:
        jogo = ' '.join(context.args)
        resposta = analisar_jogo_especifico(jogo)
        update.message.reply_text(resposta)
    else:
        update.message.reply_text("❗ Use assim: /analise Flamengo x Grêmio")

def prever(update: Update, context: CallbackContext):
    if context.args:
        jogo = ' '.join(context.args)
        resposta = prever_resultado(jogo)
        update.message.reply_text(resposta)
    else:
        update.message.reply_text("❗ Use assim: /prever Flamengo x Grêmio")

def analise_diaria(context: CallbackContext):
    hoje = datetime.date.today()
    texto = analisar_jogos_hoje(hoje)
    context.bot.send_message(chat_id=context.job.context, text=texto)

# ============ MAIN ============
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("analise", analise))
    dp.add_handler(CommandHandler("prever", prever))

    # Agendador diário às 9h
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        analise_diaria,
        trigger='cron',
        hour=9,
        minute=0,
        context=updater.bot.get_me().id  # Enviar no chat do próprio bot (ajuste se necessário)
    )

    print("🤖 Bot iniciado com polling...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
