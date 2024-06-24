import logging
import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from aiogram import Bot
from app.database import get_channels, get_keywords

load_dotenv()
logging.basicConfig(level=logging.INFO)

async def start_telegram_client(bot, user_id):
    channels = get_channels(user_id)  # Передаем user_id в функцию для получения каналов
    keywords = get_keywords()  # Функция извлечения ключевых слов из базы данных

    async with TelegramClient('session_name', os.getenv('API_ID'), os.getenv('API_HASH'),
                              device_model="Linux 5.15.0", system_version="Ubuntu 20.04.6 LTS") as client:
        for channel_link in channels:
            @client.on(events.NewMessage(chats=channel_link))
            async def handle_new_message(event):
                logging.info(f"Новое сообщение в канале {channel_link}: {event.message.message}")
                print(f"Новое сообщение в канале {channel_link}: {event.message.message}")

                # Проверяем сообщение на наличие ключевых слов
                for keyword in keywords:
                    if keyword.lower() in event.message.message.lower():
                        logging.info(f"Обнаружено ключевое слово '{keyword}' в сообщении: {event.message.message}")
                        await bot.send_message(chat_id=os.getenv('TELEGRAM_CHAT_ID'),
                                               text=f"Обнаружено ключевое слово '{keyword}' в сообщении: {event.message.message}")
                        break  # Прекращаем проверку на другие ключевые слова

            logging.info(f"Мониторинг канала {channel_link}")

        logging.info("Сессия Telethon подключена")
        
        # Запускаем клиента Telegram и ждем событий
        await client.run_until_disconnected()

def run_telegram_monitoring(bot, user_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_telegram_client(bot, user_id))
