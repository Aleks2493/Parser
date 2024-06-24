import logging
import asyncio
import os
from threading import Thread
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from app.handlers import router
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from app.parser import run_telegram_monitoring

# Включаем логирование
logging.basicConfig(level=logging.INFO)

async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TELEGRAM_TOKEN'), default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    telethon_thread = Thread(target=run_telegram_monitoring, daemon=True)
    telethon_thread.start()

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        print('Бот работает')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен')