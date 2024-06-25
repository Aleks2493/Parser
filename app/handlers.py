import app.keyboards as kb 
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from app.database import init_db, add_channels, remove_channels, add_keywords, remove_keywords, get_keywords, get_channels

router = Router()
init_db()

class AddLinkStates(StatesGroup):
    link = State()

class AddKeywordStates(StatesGroup):
    keyword = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет! Я бот для мониторинга каналов и чатов.", reply_markup=kb.main)

@router.message(F.text == "Добавление ссылки")
async def add_link_start(message: Message, state: FSMContext):
    await message.answer(f'Введите ссылку на чат. Вы можете вводить несколько ссылок, разделяя их запятой. Когда закончите, нажмите "Завершить".', reply_markup=kb.done)
    await state.set_state(AddLinkStates.link)

@router.message(AddLinkStates.link)
async def add_link_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    chat_links = message.text.split(',')
    valid_links = []
    invalid_links = []
    for link in chat_links:
        link = link.strip()
        if link.startswith("https://t.me/"):
            valid_links.append(link)
        else:
            invalid_links.append(link)
    if valid_links:
        add_channels(user_id, valid_links)
        await message.answer(f"Добавлены ссылки: {', '.join(valid_links)}", reply_markup=kb.done)
    if invalid_links:
        await message.answer(f"Неверные ссылки: {', '.join(invalid_links)}. Пожалуйста, введите ссылки в формате 'https://t.me/your_chat'.")

@router.message(F.text == "Добавление ключевых слов")
async def add_keyword_start(message: Message, state: FSMContext):
    await message.answer(f'Введите ключевые слова для мониторинга. Вы можете вводить несколько слов, разделяя их запятой. Когда закончите, нажмите "Завершить".', reply_markup=kb.done)
    await state.set_state(AddKeywordStates.keyword)

@router.message(AddKeywordStates.keyword)
async def add_keyword_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    keywords = message.text.split(',')
    add_keywords(user_id, keywords)
    await message.answer(f'Ключевые слова добавлены. Можете ввести еще слова или нажмите "Завершить".', reply_markup=kb.done)

@router.callback_query(F.data == 'end')
async def add_link_done(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await callback.message.answer(f"Добавление завершено.", reply_markup=kb.main)

@router.message(F.text == "Удаление ссылки")
async def remove_link_handler(message: Message):
    user_id = message.from_user.id
    chat_links = message.text.replace('Удаление ссылки', '').strip().split(',')

    # Проверка и отладка
    print(f"Пользователь: {user_id}")
    print(f"Исходное сообщение: {message.text}")
    print(f"Ссылки для удаления: {chat_links}")

    existing_channels = get_channels(user_id)
    print(f"Текущие ссылки на каналы для пользователя {user_id}: {existing_channels}")

    links_to_remove = [link.strip() for link in chat_links if link.strip() in existing_channels]

    if links_to_remove:
        remove_channels(user_id, links_to_remove)
        await message.answer(f"Ссылки на чаты удалены: {', '.join(links_to_remove)}", reply_markup=kb.main)
    else:
        await message.answer("Указанные ссылки на чаты не найдены в вашем списке.", reply_markup=kb.main)



@router.message(F.text == "Удаление ключевых слов")
async def remove_keyword_handler(message: Message):
    user_id = message.from_user.id
    keywords = message.text.split(',')[1:]
    existing_keywords = get_keywords(user_id)
    print(f"Текущие ключевые слова для пользователя {user_id}: {existing_keywords}")
    keywords_to_remove = [keyword.strip() for keyword in keywords if keyword.strip() in existing_keywords]
    if keywords_to_remove:
        remove_keywords(user_id, keywords_to_remove)
        await message.answer(f"Ключевые слова удалены: {', '.join(keywords_to_remove)}", reply_markup=kb.main)
    else:
        await message.answer("Указанные ключевые слова не найдены в вашем списке.", reply_markup=kb.main)

@router.message(F.text == "Список слов")
async def list_keywords_handler(message: Message):
    user_id = message.from_user.id
    keywords = get_keywords(user_id)
    if keywords:
        await message.answer(f"Ваши ключевые слова: {', '.join(keywords)}", reply_markup=kb.main)
    else:
        await message.answer("У вас нет ключевых слов для мониторинга.", reply_markup=kb.main)

@router.message(F.text == "Список ссылок")
async def list_links_handler(message: Message):
    user_id = message.from_user.id
    channels = get_channels(user_id)
    if channels:
        await message.answer(f"Ваши ссылки на чаты: {', '.join(channels)}", reply_markup=kb.main)
    else:
        await message.answer("У вас нет ссылок на чаты для мониторинга.", reply_markup=kb.main)
