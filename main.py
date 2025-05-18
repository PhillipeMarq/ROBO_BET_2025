
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
from utils.analysis import analisar_jogos_antecipados, analisar_partida_especifica
from utils.prediction import prever_resultado_partida
from utils.telegram_utils import send_message
from datetime import datetime

# Token diretamente no código (o seu token atualizado)
TOKEN = "8124502590:AAHOzEYywnp6sNuEyDn9Lz4ZNyMIIfF8RiM"

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Comando /start
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""🤖 Olá! Sou o Robô de Análises Esportivas com IA!

Use:
/analise - Para ver todos os jogos analisados dos próximos dias.
/analise [time1 x time2] - Para analisar uma partida específica.
/prever [time1 x time2] - Para prever o resultado de uma partida com IA.

Bons lucros e boas apostas! ⚽📊"""
    )

# Comando /analise
def analise(update, context):
    if len(context.args) == 0:
        jogos_analise = analisar_jogos_antecipados()
        context.bot.send_message(chat_id=update.effective_chat.id, text=jogos_analise)
    else:
        nome_partida = " ".join(context.args)
        analise = analisar_partida_especifica(nome_partida)
        context.bot.send_message(chat_id=update.effective_chat.id, text=analise)

# Comando /prever
def prever(update, context):
    if len(context.args) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="❌ Você precisa informar o jogo. Ex: /prever Flamengo x Grêmio")
    else:
        nome_partida = " ".join(context.args)
        resultado = prever_resultado_partida(nome_partida)
        context.bot.send_message(chat_id=update.effective_chat.id, text=resultado)

# Registrar os comandos
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("analise", analise))
dispatcher.add_handler(CommandHandler("prever", prever))

# Agendar envio diário automático às 9h
scheduler = BackgroundScheduler()
scheduler.add_job(lambda: send_message("🤖 Enviando análise diária dos jogos:\n\n" + analisar_jogos_antecipados()),
                  trigger='cron', hour=9, minute=0)
scheduler.start()

print("🤖 Robô iniciado com sucesso!")
updater.start_polling()
updater.idle()
