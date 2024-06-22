import logging
import asyncio
import os
from dotenv import load_dotenv
from threading import Thread
from telethon import TelegramClient, events
from app.database import get_channels, get_keywords, get_all_users
from aiogram import Bot


async def notify_user(bot, user_id, message):
    await bot.send_message(user_id, message, parse_mode='Markdown')

async def monitor_groups(client, bot):
    @client.on(events.NewMessage)
    async def handler(event):
        try:
            chat_id = event.chat_id
            message_text = event.message.message
            user_id = event.sender_id

            users = get_all_users()
            for user in users:
                channels = get_channels(user)
                keywords = get_keywords(user)

                if chat_id in channels:
                    if any(keyword.lower() in message_text.lower() for keyword in keywords):
                        chat_info = f"Чат: {chat_id}"
                        user_info = f"Пользователь: {user_id}"
                        message_link = f"https://t.me/{event.chat.username}/{event.message.id}"
                        notification_message = f"Найдено ключевое слово!\n{chat_info}\n{user_info}\n[Ссылка на сообщение]({message_link})"
                        await notify_user(bot, user, notification_message)

        except Exception as e:
            logging.error(f"Ошибка при мониторинге канала: {e}")

async def start_telethon_client(loop, bot):
    load_dotenv()
    client = TelegramClient('session_name', os.getenv('API_ID'), os.getenv('API_HASH'), loop=loop)
    await client.start()
    await monitor_groups(client, bot)
    print("Начинаем мониторинг...")
    await client.run_until_disconnected()

def run_telethon_client(bot):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_telethon_client(loop, bot))