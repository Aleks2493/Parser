from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавление ссылки'),KeyboardButton(text='Добавление ключевых слов')],
    [KeyboardButton(text='Удаление ссылки'),KeyboardButton(text='Удаление ключевых слов')],
    [KeyboardButton(text='Список ссылок'),KeyboardButton(text='Список слов')],
],resize_keyboard=True,one_time_keyboard=True
)

done = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Завершить', callback_data='end')],
],resize_keyboard=True
)

contacts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Группа телеграмм', url='https://t.me/BotCraftAI'),InlineKeyboardButton(text='Наш сайт', url='https://kolizey-fit.ru/')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
],resize_keyboard=True
)

ai = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад')]
],resize_keyboard=True, input_field_placeholder='Вернуться в меню нажмите "Назад"',one_time_keyboard=True               
)