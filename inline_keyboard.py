from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

B_START = InlineKeyboardButton('Начать', callback_data='songs_list')
B_EXAMPLE = InlineKeyboardButton('Примеры файлов', callback_data='example')

B_YES = InlineKeyboardButton('Да, верно', callback_data='background')
B_NO = InlineKeyboardButton('Нет, переделать', callback_data='songs_list')

START = InlineKeyboardMarkup().add(B_START, B_EXAMPLE)
CHECK_SONGS = InlineKeyboardMarkup().add(B_YES, B_NO)
