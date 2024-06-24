import logging
import asyncio
import os
import json
from telethon import connection
from dotenv import load_dotenv
from threading import Thread
from telethon import TelegramClient, events
from aiogram import Bot
# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest


load_dotenv()
logging.basicConfig(level=logging.INFO)

async def dump_all_messages():
	client = TelegramClient('session_name', os.getenv('API_ID'), os.getenv('API_HASH'), loop=loop)
	await client.start()
	channel = 2208551919
	"""Записывает json-файл с информацией о всех сообщениях канала/чата"""
	offset_msg = 0    # номер записи, с которой начинается считывание
	limit_msg = 100   # максимальное число записей, передаваемых за один раз

	all_messages = []   # список всех сообщений
	total_messages = 0
	total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

	class DateTimeEncoder(json.JSONEncoder):
		'''Класс для сериализации записи дат в JSON'''
		def default(self, o):
			if isinstance(o, datetime):
				return o.isoformat()
			if isinstance(o, bytes):
				return list(o)
			return json.JSONEncoder.default(self, o)

	while True:
		history = await client(GetHistoryRequest(
			peer=channel,
			offset_id=offset_msg,
			offset_date=None, add_offset=0,
			limit=limit_msg, max_id=0, min_id=0,
			hash=0))
		if not history.messages:
			break
		messages = history.messages
		for message in messages:
			all_messages.append(message.to_dict())
		offset_msg = messages[len(messages) - 1].id
		total_messages = len(all_messages)
		if total_count_limit != 0 and total_messages >= total_count_limit:
			break

	with open('channel_messages.json', 'w', encoding='utf8') as outfile:
		 json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)



def run_telegram_monitoring():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(dump_all_messages(loop))

# async def monitor_channel(client, bot, channel_link):
#     try:
#         entity = await client.get_entity(channel_link)
#         channel_id = entity.id

#         print(f'Канал: {channel_id}')
#         # Преобразуем channel_id в формат -100xxxxxxxxxx
#         if channel_id > 0:
#             channel_id = int(f'-100{channel_id}')
#         print(f'Канал после: {channel_id}')

#         @client.on(events.NewMessage)
#         async def handler(event):
#             print(event.chat.name, ':', event.text)

#             messages = client.get_messages(channel_id, 1)
#             print(messages)
#             try:
#                 message = event.message
#                 message_text = message.message if message else None

#                 logging.info(f"Получено сообщение: {message_text} в канале {channel_link}")

#                 if message_text:
#                     logging.info(f"Сообщение: {message_text}")
#                 else:
#                     logging.info("Сообщение не содержит текста.")
#             except Exception as e:
#                 logging.error(f"Ошибка при обработке сообщения: {e}")

#     except Exception as e:
#         logging.error(f"Ошибка при мониторинге канала: {e}")

# async def start_telegram_client(loop):
#     client = TelegramClient('session_name', os.getenv('API_ID'), os.getenv('API_HASH'), loop=loop)
#     await client.start()
#     print("Сессия подключена...")
#     id_channel = 2208551919
    
#     last_message = await client.get_entity(id_channel)
#     last_message2 = await client.get_input_entity(id_channel)
#     entity = await client.get_entity('someone')
#     last_message3 = await client.get_messages(id_channel, 0)
#     # async for message in client.iter_messages(id_channel):
#     #     print(message.id, message.text)


#     if last_message:
#         print(f"Последнее сообщение1: {last_message}")
#         print(f"Последнее сообщение2: {last_message2}")
#         print(f"Последнее сообщение3: {entity}")
#         print(f"Последнее сообщение4: {last_message3}")
#     else:
#         print("Сообщений нет")

#     print("Начинаем мониторинг...")
    # await client.run_until_disconnected()