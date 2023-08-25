import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, callback_query
from players import parse_info, get_link

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands='start')
async def start_process(message):
    await message.answer('Hello! Enter your favourite football player(Name and Surname): ')


@dp.message_handler(content_types='text')
async def get_player_info(message: types.Message):
    query = message.text.title()
    link = get_link(query)
    player_info = parse_info(link)
    response = (
        f"\nFull Name: {player_info['name_surname']}\nShirt Number: {player_info['shirt_number']}\nDate of birth: {player_info['date_of_birth']}\nNationality: {player_info['nationality']}\nClub: {player_info['club']}\nTransfer value: {player_info['transfer_price']}")
    await message.answer(response)


if __name__ == '__main__':
    executor.start_polling(dp)
