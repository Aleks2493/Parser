import logging
import asyncio
import os
from functools import partial
from dotenv import load_dotenv
from telethon import TelegramClient, events
from aiogram import Bot

from app.database import get_all_users, get_channels, get_keywords

load_dotenv()
logging.basicConfig(level=logging.INFO)

# Здесь необходимо указать ваш токен API Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Инициализация бота
bot = Bot(token=TELEGRAM_TOKEN)

async def handle_new_message(channel_link, user_id, client, event):
    try:
        # Получаем информацию о канале и отправителе
        channel = await client.get_entity(channel_link)
        sender = await client.get_entity(event.message.sender_id)

        # Получаем ключевые слова
        keywords = get_keywords(user_id)

        # Проверка ключевых слов в сообщении
        message_text = event.message.message.lower()
        if any(keyword.lower() in message_text for keyword in keywords):
            # Формируем сообщение
            message = f"Новое сообщение в канале: {channel.title}, от пользователя: {sender.first_name} {sender.last_name or ''}: {event.message.message}\n"
            message += f"Ссылка на сообщение: https://t.me/{channel.username}/{event.message.id}"
            
            # Отправляем сообщение в Telegram
            await bot.send_message(chat_id=user_id, text=message)

            logging.info(f"Найдено ключевое слово в канале {channel.title}: {event.message.message}")
            print(f"Найдено ключевое слово в канале {channel.title}: {event.message.message}")
    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")
        print(f"Ошибка при обработке сообщения: {e}")

async def start_telegram_client(loop):
    users = get_all_users()  # Получаем список пользователей из базы данных

    async with TelegramClient('session_name', os.getenv('API_ID'), os.getenv('API_HASH'), device_model="Linux 5.15.0", system_version="Ubuntu 20.04.6 LTS", loop=loop) as client:
        for user_id in users:
            channels = get_channels(user_id)  # Получаем каналы для текущего пользователя
            for channel_link in channels:
                client.add_event_handler(partial(handle_new_message, channel_link, user_id, client), events.NewMessage(chats=channel_link))

        logging.info("Сессия Telethon подключена")
        
        # Запускаем клиента Telegram и ждем событий
        await client.run_until_disconnected()

def run_telegram_monitoring():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_telegram_client(loop))
    loop.close()
