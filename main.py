import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from analise_jogos import analisar_jogos_hoje, analisar_jogo_especifico
from previsor_ia import prever_resultado

# ============ CONFIG ============
TOKEN = "8124502590:AAHOzEYywnp6sNuEyDn9Lz4ZNyMIIfF8RiM"
CHAT_ID_TESTE = 7178592047  # Seu chat ID direto

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ============ COMANDOS ============
def start(update: Update, context: CallbackContext):
    logging.info(f"✅ Comando /start recebido de {update.effective_user.username}")
    update.message.reply_text("👋 Olá! Robô de apostas esportivas ativo.")

def analise(update: Update, context: CallbackContext):
    logging.info("📥 Comando /analise recebido")
    if context.args:
        jogo = ' '.join(context.args)
        resposta = analisar_jogo_especifico(jogo)
        update.message.reply_text(resposta)
    else:
        update.message.reply_text("❗ Use assim: /analise Flamengo x Grêmio")

def prever(update: Update, context: CallbackContext):
    logging.info("📥 Comando /prever recebido")
    if context.args:
        jogo = ' '.join(context.args)
        resposta = prever_resultado(jogo)
        update.message.reply_text(resposta)
    else:
        update.message.reply_text("❗ Use assim: /prever Flamengo x Grêmio")

def analise_diaria(context: CallbackContext):
    hoje = datetime.date.today()
    texto = analisar_jogos_hoje(hoje)
    logging.info("📤 Enviando análise automática diária")
    context.bot.send_message(chat_id=CHAT_ID_TESTE, text=texto)

# ============ MAIN ============
def main():
    logging.info("🚀 Iniciando bot em modo polling...")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("analise", analise))
    dp.add_handler(CommandHandler("prever", prever))

    # Agendamento da análise diária
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        analise_diaria,
        trigger='cron',
        hour=9,
        minute=0,
        context=updater.bot.get_me().id
    )

    updater.start_polling()
    logging.info("📡 Bot rodando... aguardando comandos.")
    updater.idle()

if __name__ == '__main__':
    main()
