from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
from .analysis import analisar_jogos_antecipados, analisar_partida_especifica
from .prediction import prever_resultado_partida
from .telegram_utils import send_message
from datetime import datetime

# ✅ TOKEN direto (você disse que está usando assim mesmo)
TOKEN = "8124502590:AAHOzEYywnp6sNuEyDn9Lz4ZNyMIIfF8RiM"

# ✅ Função de boas-vindas
def start(update, context):
    mensagem = (
        "🤖 Olá! Sou o Robô de Análises Esportivas com IA!\n"
        "Use /analise para ver os jogos analisados.\n"
        "Use /analise [time1 x time2] para analisar uma partida específica.\n"
        "Use /prever [time1 x time2] para prever o resultado de uma partida com IA."
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem)

# ✅ Comando para analisar os próximos jogos
def analise_command(update, context):
    if context.args:
        nome_partida = " ".join(context.args)
        mensagem = analisar_partida_especifica(nome_partida)
    else:
        mensagem = analisar_jogos_antecipados()
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem)

# ✅ Comando para prever resultado de uma partida com IA
def prever_command(update, context):
    if context.args:
        nome_partida = " ".join(context.args)
        mensagem = prever_resultado_partida(nome_partida)
    else:
        mensagem = "❌ Por favor, use o formato: /prever time1 x time2"
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem)

# ✅ Enviar automaticamente todos os dias às 9h
def tarefa_diaria():
    mensagem = analisar_jogos_antecipados()
    send_message(mensagem)

# ✅ Inicialização do bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("analise", analise_command))
    dispatcher.add_handler(CommandHandler("prever", prever_command))

    # Agendamento da tarefa diária
    scheduler = BackgroundScheduler()
    scheduler.add_job(tarefa_diaria, trigger='cron', hour=9, minute=0)
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
