from aiogram.fsm.state import State, StatesGroup

class Phone(StatesGroup):
    add_phone = State()
    remove_phone = State()