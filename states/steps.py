from aiogram.dispatcher.filters.state import StatesGroup, State


class Choice(StatesGroup):
   search = State()
   choice = State()
   favourite = State()
   info = State()

