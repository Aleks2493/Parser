import logging
import asyncio
import os
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from aiogram import Bot
from app.database import get_all_users, get_channels, get_keywords
    
client = TelegramClient('anon', token=os.getenv('YOUR_API_ID'), token=os.getenv('YOUR_API_HASH'))

async def monitor_groups(bot: Bot):
    while True:
        users = get_all_users()  # Получаем всех пользователей
        for user_id in users:
            channels = get_channels(user_id)
            keywords = get_keywords(user_id)
            for channel in channels:
                try:
                    async with client:
                        chat = await client.get_entity(channel)
                        messages = await client(GetHistoryRequest(
                            peer=chat,
                            limit=100,
                            offset_date=None,
                            offset_id=0,
                            max_id=0,
                            min_id=0,
                            add_offset=0,
                            hash=0
                        ))
                        
                        for message in messages.messages:
                            if message.message and any(keyword.lower() in message.message.lower() for keyword in keywords):
                                chat_info = f"Чат: {chat.title if chat.title else chat.id}"
                                user_info = f"Пользователь: {message.sender_id}"
                                message_link = f"https://t.me/{chat.username}/{message.id}"
                                await bot.send_message(user_id, f"Найдено ключевое слово!\n{chat_info}\n{user_info}\n[Ссылка на сообщение]({message_link})", parse_mode='Markdown')
                except Exception as e:
                    logging.error(f"Ошибка при мониторинге канала {channel}: {e}")
        await asyncio.sleep(60)  # Ждем 60 секунд перед следующим циклом

async def start_monitoring(bot: Bot):
    await client.start()
    asyncio.create_task(monitor_groups(bot))

















# import logging
# import asyncio
# from aiogram import Bot
# from app.database import get_all_users, get_channels, get_keywords

# async def monitor_groups(bot: Bot):
#     while True:
#         users = get_all_users()  # Получаем всех пользователей
#         for user_id in users:
#             channels = get_channels(user_id)
#             keywords = get_keywords(user_id)
#             for channel in channels:
#                 try:
#                     # Получаем информацию о чате
#                     chat = await bot.get_chat(channel)
                    
#                     # Получаем историю сообщений в чате
#                     async for message in bot.get_updates(chat_id=chat.id, limit=100):
#                         if message.message and message.message.text and any(keyword.lower() in message.message.text.lower() for keyword in keywords):
#                             chat_info = f"Чат: {chat.title if chat.title else chat.id}"
#                             user_info = f"Пользователь: {message.message.from_user.full_name} ({message.message.from_user.id})"
#                             message_link = f"https://t.me/{chat.username}/{message.message.message_id}"
#                             await bot.send_message(user_id, f"Найдено ключевое слово!\n{chat_info}\n{user_info}\n[Ссылка на сообщение]({message_link})", parse_mode='Markdown')
#                 except Exception as e:
#                     logging.error(f"Ошибка при мониторинге канала {channel}: {e}")
#         await asyncio.sleep(60)  # Ждем 60 секунд перед следующим циклом
