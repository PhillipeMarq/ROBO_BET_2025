import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from analise_jogos import enviar_analises_automaticas
from prever import prever_resultado
from analise_jogos import analisar_jogo_especifico, analisar_jogos_do_dia

# Token atualizado do seu bot
TOKEN = "8124502590:AAHOzEYywnp6sNuEyDn9Lz4ZNyMIIfF8RiM"

# Setup de log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Olá! Eu sou o seu bot de análises esportivas.\n"
        "📊 Use /analise para ver análises dos próximos jogos.\n"
        "📌 Use /analise Flamengo x Grêmio para análise de um jogo específico.\n"
        "🧠 Use /prever Flamengo x Grêmio para prever o resultado com IA."
    )

# Comando /analise
async def analise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        jogo = " ".join(context.args)
        resposta = await analisar_jogo_especifico(jogo)
    else:
        resposta = await analisar_jogos_do_dia()
    await update.message.reply_text(resposta)

# Comando /prever
async def prever(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        jogo = " ".join(context.args)
        resposta = await prever_resultado(jogo)
    else:
        resposta = "❌ Por favor, envie o nome do jogo. Exemplo: /prever Flamengo x Grêmio"
    await update.message.reply_text(resposta)

# Agendamento automático diário
def iniciar_agendamentos(application):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: enviar_analises_automaticas(application), 'cron', hour=9, minute=0)
    scheduler.start()

# Função principal
async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("analise", analise))
    application.add_handler(CommandHandler("prever", prever))

    iniciar_agendamentos(application)

    await application.run_polling()

# Iniciar
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
