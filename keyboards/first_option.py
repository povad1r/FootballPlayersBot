from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_list = InlineKeyboardMarkup()
first_button = InlineKeyboardButton(text='Become favourite player', callback_data='Add')
button_list.add(first_button)
second_button = InlineKeyboardButton(text='Player info', callback_data='Info')
button_list.add(second_button)
