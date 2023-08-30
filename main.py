import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, callback_query
from players import parse_info, get_link, get_player_performance_data, get_achievements
from parse import get_match_link, get_match_info
from keyboards.first_option import button_list
from keyboards.info_kb import info_kb
import os
from dotenv import load_dotenv
from database import Database
from states.steps import Choice



load_dotenv()

TOKEN = os.getenv('TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database()

@dp.message_handler(commands='start', state='*')
async def start_process(message: types.Message):
    user = await db.check_user(message.from_id)
    if not user:
        await db.register_user(
            message.from_user.first_name,
            message.from_user.username,
            message.from_id
        )
        await message.answer('Thanks for registration')
    else:
        await message.answer(f'Hi, {message.from_user.first_name}')
    await message.answer('Enter your footballer: ')
    await Choice.search.set()

@dp.message_handler(content_types='text', state=Choice.search)
async def get_player_info(message: types.Message, state: FSMContext):
    query = message.text.title()
    link = get_link(query)
    async with state.proxy() as data:
        data['link'] = link
        data['query'] = query
    player_info = parse_info(link)
    response = (
        f"\nFull Name: {player_info['name_surname']}\nShirt Number: {player_info['shirt_number']}\nDate of birth: {player_info['date_of_birth']}\nNationality: {player_info['nationality']}\nClub: {player_info['club']}\nTransfer value: {player_info['transfer_price']}")
    await message.answer(response, reply_markup=button_list)
    await Choice.choice.set()

@dp.callback_query_handler(lambda c: c.data == 'Add', state=Choice.choice)
async def add_favourite_player(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    async with state.proxy() as data:
        query = data['query']
    await db.add_favourite_player(query, user_id)
    await bot.send_message(user_id, "Player added to favorites!") 
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'Info', state=Choice.choice)
async def show_player_info(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.edit_message_reply_markup(user_id, callback_query.message.message_id, reply_markup=info_kb)
    await Choice.info.set()

@dp.callback_query_handler(lambda c: c.data == 'Next Match', state=Choice.info)
async def next_match(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        link = data['link']
    data_match = get_match_link(link)
    content = get_match_info(data_match)
    response = (
        f"\nDate: {content['date']}\nStart of the match: {content['time']}\nTournament: {content['competition']}\n{content['home_team']} - {content['guest_team']}")
    await bot.send_message(callback_query.from_user.id, response)


@dp.callback_query_handler(lambda c: c.data == 'Performance', state=Choice.info)
async def player_performance(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        link = data['link']
    content = get_player_performance_data(link)
    response = (
        f"\nAppeareances: {content['games_played']}\nGoals: {content['goals_scored']}\nAssists: {content['assists']}\nYellow Cards: {content['yellow_cards']}\nRed Cards: {content['red_cards']}"
    )
    await bot.send_message(callback_query.from_user.id, response)

@dp.callback_query_handler(lambda c: c.data == 'Achievements', state=Choice.info)
async def player_performance(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        link = data['link']
    content = get_achievements(link)
    response = "\n".join(content)
    await bot.send_message(callback_query.from_user.id, response)

@dp.callback_query_handler(lambda c: c.data == 'Back', state=Choice.info)
async def back(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.edit_message_reply_markup(user_id, callback_query.message.message_id, reply_markup=button_list)
    await Choice.choice.set()


if __name__ == '__main__':
    executor.start_polling(dp)
