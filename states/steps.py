from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
   set_name = State()
   set_age = State()
   set_email = State()

