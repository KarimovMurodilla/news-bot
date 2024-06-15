from aiogram.fsm.state import StatesGroup, State


class CategoryGroup(StatesGroup):
    step1 = State()
    confirm = State()
