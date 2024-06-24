import logging
import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from app.database import get_channels, get_all_users, get_keywords


load_dotenv()
logging.basicConfig(level=logging.INFO)


async def start_telegram_client(loop, queue):
    users = get_all_users()  # Получаем список пользователей из базы данных

    async with TelegramClient('session_name', os.getenv('API_ID'), os.getenv('API_HASH'), device_model="Linux 5.15.0", system_version="Ubuntu 20.04.6 LTS", loop=loop) as client:
        for user_id in users:
            channels = get_channels(user_id)  # Получаем каналы для текущего пользователя
            for channel_link in channels:
                @client.on(events.NewMessage(chats=channel_link))
                async def handle_new_message(event):
                    logging.info(f"Новое сообщение в канале {channel_link}: {event.message.message}")

                    keywords = get_keywords(user_id)  # Получаем список ключевых слов из базы данных
                    print(keywords)
                    for keyword in keywords:
                        if keyword.lower() in event.message.message.lower():
                            logging.info(f"Найдено ключевое слово '{keyword}' в сообщении")
                            # Дополнительные действия по вашему выбору, например, отправка уведомления или сохранение в базу данных

                logging.info(f"Мониторинг канала {channel_link}")

        logging.info("Сессия Telethon подключена")
        
        # Запускаем клиента Telegram и ждем событий
        await client.run_until_disconnected()

def run_telegram_monitoring():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    last_message = loop.run_until_complete(start_telegram_client(loop))
    loop.close()
    return last_message



# Получение последнего сообщения!
# async def start_telegram_client(loop):
#     channel_link = "https://t.me/TestGroupsAleks"

#     async with TelegramClient('session_name', os.getenv('API_ID'), os.getenv('API_HASH'),  device_model="Linux 5.15.0", system_version="Ubuntu 20.04.6 LTS", loop=loop)  as client:
#         entity = await client.get_entity(channel_link)
#         channel_id = entity.id
#         logging.info("Сессия Telethon подключена")

#         logging.info(f"Получение последнего сообщения из канала {channel_id}")
#         channel = PeerChannel(channel_id)
#         history = await client(GetHistoryRequest(
#             peer=channel,
#             offset_id=0,
#             offset_date=None,
#             add_offset=0,
#             limit=1,
#             max_id=0,
#             min_id=0,
#             hash=0
#         ))

#         if history.messages:
#             message = history.messages[0]
#             logging.info(f"Получено последнее сообщение: {message.message}")
#             return message
#         else:
#             logging.info("Сообщений нет")
#             return None