from aiogram.fsm.state import StatesGroup, State


class AddUserForm(StatesGroup):
    user_id = State()
    user_name = State()
    need_subscription = State()
    subscription_duration = State()