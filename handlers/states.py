from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    start = State()
    warning = State()
    payment_type = State()
    payment_success = State()
