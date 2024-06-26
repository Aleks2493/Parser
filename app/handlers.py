import app.keyboards as kb 
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from app.database import init_db, add_channels, add_keywords, get_keywords, get_channels, remove_all_channels, remove_all_keywords

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
    await message.answer(f'Ключевые слова добавлены: [{', '.join(keywords)}]. Можете ввести еще слова или нажмите "Завершить".', reply_markup=kb.done)

@router.callback_query(F.data == 'end')
async def add_link_done(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await callback.message.answer(f"Добавление завершено.", reply_markup=kb.main)

@router.message(F.text == "Удаление ссылки")
async def remove_all_links_confirm(message: Message):
    await message.answer("Точно всё удалить? Вернуться будет невозможно!", reply_markup=kb.confirmation_links)

@router.callback_query(F.data == 'confirm_delete_links')
async def confirm_delete_links(callback: CallbackQuery):
    user_id = callback.from_user.id
    remove_all_channels(user_id)
    await callback.message.answer("Все ссылки на чаты удалены.", reply_markup=kb.main)
    await callback.answer()

@router.callback_query(F.data == 'cancel_delete_links')
async def cancel_delete_links(callback: CallbackQuery):
    await callback.message.answer("Удаление отменено.", reply_markup=kb.main)
    await callback.answer()

@router.message(F.text == "Удаление ключевых слов")
async def remove_all_keywords_confirm(message: Message):
    await message.answer("Точно всё удалить? Вернуться будет невозможно!", reply_markup=kb.confirmation_keywords)

@router.callback_query(F.data == 'confirm_delete_keywords')
async def confirm_delete_keywords(callback: CallbackQuery):
    user_id = callback.from_user.id
    remove_all_keywords(user_id)
    await callback.message.answer("Все ключевые слова удалены.", reply_markup=kb.main)
    await callback.answer()

@router.callback_query(F.data == 'cancel_delete_keywords')
async def cancel_delete_keywords(callback: CallbackQuery):
    await callback.message.answer("Удаление отменено.", reply_markup=kb.main)
    await callback.answer()

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
