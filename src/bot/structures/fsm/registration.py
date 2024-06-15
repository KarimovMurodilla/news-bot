from aiogram.fsm.state import StatesGroup, State


class RegisterGroup(StatesGroup):
    lang = State()
    fullname = State()
    phone_number = State()
    region = State()

    receive_cashback_id = State()
