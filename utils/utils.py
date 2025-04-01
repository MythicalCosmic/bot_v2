from database.models import User, PaymentMovement
from database.database import SessionLocal
from aiogram.types import ChatInviteLink
from config.settings import TIMEZONE
import traceback
import pytz
from datetime import datetime

timezone = pytz.timezone(TIMEZONE)

def user_exists(user_id: int) -> bool:
    db = SessionLocal()
    try:
        exists = db.query(User).filter(User.id == user_id).first() is not None
        return exists
    finally:
        db.close()

        
def add_user(user_id: int, first_name: str, last_name: str | None, username: str | None):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.id == user_id).first()
    
    if not existing_user:
        user = User(id=user_id, first_name=first_name, last_name=last_name, username=username)
        db.add(user)
        db.commit()
    
    db.close()

def add_to_payment_movements(user_id: int, generated_link: str, total_price: float, payment_type: str):
    db = SessionLocal()
    payment_movement = PaymentMovement(telegram_id=user_id, generated_link=generated_link, total_price=total_price, payment_type=payment_type)
    db.add(payment_movement)
    db.commit()
    db.refresh(payment_movement)
    return payment_movement.id

def set_user_state(user_id: int, state: str):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    
    if user:
        user.state = state
        db.commit()
    
    db.close()

def get_user_state(user_id: int) -> str | None:
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    
    return user.state if user else None


async def generate_one_time_link(bot, channel_username: str):
    try:
        chat_invite_link: ChatInviteLink = await bot.create_chat_invite_link(
            chat_id=channel_username, 
            member_limit=1 
        )
        return chat_invite_link.invite_link  
    except Exception as e:
        return None
    
def format_error(context, message, error, user_id=None):
    base_info = f"❌ {context.capitalize()} error:\n"
    if message:
        base_info += (
            f"User ID: {message.from_user.id}\n"
            f"Username: @{message.from_user.username or 'N/A'}\n"
            f"Message Text: {message.text if hasattr(message, 'text') else 'N/A'}\n"
        )
    elif user_id:
        base_info += f"User ID: {user_id}\n"
    
    return (
        f"{base_info}"
        f"Error Type: {type(error).__name__}\n"
        f"Error Message: {str(error)}\n"
        f"Traceback:\n{traceback.format_exc()}"
    )

def format_payment_success(message, total_price, payment_type, generated_link, payment_movement_id):
    current_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
    formatted_price = f"{total_price:,.2f}"
    return (
        f"✅ Muvaffaqiyatli to'lov qabul qilindi!\n\n"
        f"To'lov ID: #{payment_movement_id}\n"
        f"User ID: {message.from_user.id}\n"
        f"Username: @{message.from_user.username or ''}\n"
        f"FIO: {message.from_user.first_name} {message.from_user.last_name or ''}\n"
        f"Summa: {formatted_price} {message.successful_payment.currency}\n"
        f"To'lov usuli: #{payment_type}\n"
        f"Link: {generated_link}\n"
        f"Sana: {current_time}\n"
    )