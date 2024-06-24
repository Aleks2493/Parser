import logging
import asyncio
import os
import json
from telethon import connection
from dotenv import load_dotenv
from threading import Thread
from telethon import TelegramClient, events
from aiogram import Bot



async def monitor_channel(client, channel_link):
    try:
        entity = await client.get_entity(channel_link)
        channel_id = entity.id

        @client.on(events.NewMessage)
        async def handler(event):
            print(event.chat.name, ':', event.text)

            messages = client.get_messages(channel_id, 1)
            print(messages)
            try:
                message = event.message
                message_text = message.message if message else None

                logging.info(f"Получено сообщение: {message_text} в канале {channel_link}")

                if message_text:
                    logging.info(f"Сообщение: {message_text}")
                else:
                    logging.info("Сообщение не содержит текста.")
            except Exception as e:
                logging.error(f"Ошибка при обработке сообщения: {e}")

    except Exception as e:
        logging.error(f"Ошибка при мониторинге канала: {e}")

async def start_telegram_client(loop):
    client = TelegramClient('session_name', os.getenv('API_ID'), os.getenv('API_HASH'), loop=loop)
    await client.start()
    print("Сессия подключена...")
    id_channel = 2208551919
    
    last_message = await client.get_entity(id_channel)
    last_message2 = await client.get_input_entity(id_channel)
    entity = await client.get_entity('someone')
    last_message3 = await client.get_messages(id_channel, 0)
    # async for message in client.iter_messages(id_channel):
    #     print(message.id, message.text)


    if last_message:
        print(f"Последнее сообщение1: {last_message}")
        print(f"Последнее сообщение2: {last_message2}")
        print(f"Последнее сообщение3: {entity}")
        print(f"Последнее сообщение4: {last_message3}")
    else:
        print("Сообщений нет")

    print("Начинаем мониторинг...")
    await client.run_until_disconnected()