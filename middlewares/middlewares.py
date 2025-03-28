from aiogram import BaseMiddleware
from aiogram.types import Message
from utils.utils import add_user, set_user_state, user_exists  
from keyboards.keyboards import main_menu_keyboard
from config.settings import get_translation
from handlers.states import UserStates

class UserRegistrationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        first_name = event.from_user.first_name
        last_name = event.from_user.last_name
        username = event.from_user.username
        
        if not user_exists(user_id):
            add_user(user_id, first_name, last_name, username)
            set_user_state(user_id, UserStates.start.state)
            
            await event.answer(
                get_translation('start_message'),
                reply_markup=main_menu_keyboard(),
                parse_mode='HTML'
            )
            state = data['state']
            await state.set_state(UserStates.start)
            return 
        
        return await handler(event, data)