import logging
import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from app.handlers import router
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from app.parser import start_monitoring

# Включаем логирование
logging.basicConfig(level=logging.INFO)

async def main():       
    load_dotenv()   
    bot = Bot(token=os.getenv('TELEGRAM_TOKEN'), default=DefaultBotProperties(parse_mode='HTML'))         #Подключение к боту по токену, при Proxy добавить (, session=session)
    dp = Dispatcher(storage=MemoryStorage())  
    dp.include_router(router)
    asyncio.create_task(start_monitoring(bot))
    await dp.start_polling(bot)          #Отправляют запрос на сервер ТГ, если ответ есть, то он вернет его.


if __name__ == '__main__':               
    try:                                 
        print('Бот работает')  
        asyncio.run(main())       
    except KeyboardInterrupt:
        print('Бот остановлен')