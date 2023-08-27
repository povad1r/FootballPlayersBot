from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_list = InlineKeyboardMarkup()
first_button = InlineKeyboardButton(text='Next Match', callback_data='Next Match')
button_list.add(first_button)
second_button = InlineKeyboardButton(text='Player Performance', callback_data='Performance')
button_list.add(second_button)
