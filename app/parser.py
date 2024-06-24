import logging
import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from app.database import get_all_users, get_channels, get_keywords
from aiogram import Bot

load_dotenv()
logging.basicConfig(level=logging.INFO)

# Здесь необходимо указать ваш токен API Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start_telegram_client(loop):
    users = get_all_users()  # Получаем список пользователей из базы данных

    async with TelegramClient('session_name', os.getenv('API_ID'), os.getenv('API_HASH'), device_model="Linux 5.15.0", system_version="Ubuntu 20.04.6 LTS", loop=loop) as client:
        for user_id in users:
            channels = get_channels(user_id)  # Получаем каналы для текущего пользователя
            for channel_link in channels:
                @client.on(events.NewMessage(chats=channel_link))
                async def handle_new_message(event):
                    logging.info(f"Новое сообщение в канале {channel_link}: {event.message.message}")

                    keywords = get_keywords(user_id)  # Получаем список ключевых слов из базы данных
                    for keyword in keywords:
                        if keyword.lower() in event.message.message.lower():
                            logging.info(f"Найдено ключевое слово '{keyword}' в сообщении")


                            # Отправляем сообщение в бота
                            await send_to_bot(user_id, channel_link, event.message.message)

                logging.info(f"Мониторинг канала {channel_link}")

        logging.info("Сессия Telethon подключена")
        
        # Запускаем клиента Telegram и ждем событий
        await client.run_until_disconnected()

async def send_to_bot(user_id, channel_link, message):
    # Функция для отправки сообщения в бота

    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        await bot.send_message(user_id, f"Новое сообщение в канале: {channel_link}, от пользователя:{user_id}:\n{message}")
        logging.info(f"Сообщение успешно отправлено в бота пользователю {user_id}")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения в бота: {e}")

def run_telegram_monitoring():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    last_message = loop.run_until_complete(start_telegram_client(loop))
    loop.close()
    return last_message
