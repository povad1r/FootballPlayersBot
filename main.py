import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, callback_query
from players import parse_info, get_link, get_player_performance_data
from parse import get_match_link, get_match_info
from keyboards.first_option import button_list
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
    global link
    query = message.text.title()
    link = get_link(query)
    player_info = parse_info(link)
    response = (
        f"\nFull Name: {player_info['name_surname']}\nShirt Number: {player_info['shirt_number']}\nDate of birth: {player_info['date_of_birth']}\nNationality: {player_info['nationality']}\nClub: {player_info['club']}\nTransfer value: {player_info['transfer_price']}")
    await message.answer(response, reply_markup=button_list)


@dp.callback_query_handler(lambda c: c.data == 'Next Match')
async def next_match(callback_query: types.CallbackQuery):
    data_match = await get_match_link(link)
    content = await get_match_info(data_match)
    response = (
        f"\nDate: {content['date']}\nStart of the match: {content['time']}\nTournament: {content['competition']}\n{content['home_team']} - {content['guest_team']}")
    await bot.send_message(callback_query.from_user.id, response)


@dp.callback_query_handler(lambda c: c.data == 'Performance')
async def player_performance(callback_query: types.CallbackQuery):
    content = get_player_performance_data(link)
    response = (
        f"\nAppeareances: {content['games_played']}\nGoals: {content['goals_scored']}\nAssists: {content['assists']}\nYellow Cards: {content['yellow_cards']}\nRed Cards: {content['red_cards']}"
    )
    await bot.send_message(callback_query.from_user.id, response)

if __name__ == '__main__':
    executor.start_polling(dp)
