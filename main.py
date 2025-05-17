import asyncio
from aiogram import Bot, Dispatcher
from handlers import router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from diario import enviar_analises_diarias
import logging
import os

# Ativar logs
logging.basicConfig(level=logging.INFO)

# Obter token do ambiente
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Criar bot e dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(router)

# Criar agendador
scheduler = AsyncIOScheduler()

# Agendar tarefa diária às 9h
scheduler.add_job(enviar_analises_diarias, CronTrigger(hour=9, minute=0))

async def main():
    scheduler.start()
    logging.info("Bot iniciado com sucesso.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
