from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

info_kb = InlineKeyboardMarkup()
first_button = InlineKeyboardButton(text='Next Match', callback_data='Next Match')
second_button = InlineKeyboardButton(text='Player Performance', callback_data='Performance')
third_button = InlineKeyboardButton(text='Achievements', callback_data='Achievements')
info_kb.add(first_button, second_button, third_button)
back_button = InlineKeyboardButton(text='Back', callback_data='Back')
info_kb.add(back_button)
