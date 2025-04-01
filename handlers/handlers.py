from aiogram import Router, Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from .states import UserStates
from config.settings import get_translation, CLICK_TOKEN, PAYME_TOKEN, ADMIN_ID, LINK_CHANNEL_ID,ADMINS_GROUP_ID, VIDEO_MESSAGE_ID,PDF_MESSAGE_ID, SOURCE_CHANNEL_ID
from utils.utils import set_user_state, format_error, generate_one_time_link, add_to_payment_movements, format_payment_success
from keyboards.keyboards import *

router = Router()

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        set_user_state(user_id, UserStates.start.state)
        await bot.copy_message(chat_id=message.chat.id, from_chat_id=SOURCE_CHANNEL_ID, message_id=VIDEO_MESSAGE_ID)
        await message.reply(
            get_translation('start_message'),
            reply_markup=main_menu_keyboard(),
            parse_mode='HTML'
        )
        await message.answer(get_translation('free_knowledge_message'),parse_mode='HTML')
        await state.set_state(UserStates.start)
    except Exception as e:
        await bot.send_message(ADMIN_ID, format_error("start", message, e))

@router.message(lambda message: message.text == JOIN_PREMIUM_CHANNEL, StateFilter(UserStates.start))
async def handle_warning(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    try:
        set_user_state(user_id, UserStates.warning.state)
        await message.reply(
            get_translation('warning_message'),
            reply_markup=confirmation_keyboard(),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.warning)   
    except Exception as e:
        await bot.send_message(ADMIN_ID, format_error("handle_warning", message, e))

@router.message(lambda message: message.text == CONFIRM_JOIN, StateFilter(UserStates.warning))
async def handle_okay(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    try:
        set_user_state(user_id, UserStates.payment_type.state)
        await message.reply(
            get_translation('payment_type_message'),
            reply_markup=payment_options_keyboard(),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.payment_type)   
    except Exception as e:
        await bot.send_message(ADMIN_ID, format_error("handle_okay", message, e))

@router.message(lambda message: message.text in [PAYMENT_CLICK, PAYMENT_PAYME], StateFilter(UserStates.payment_type))
async def handle_payment(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    payment_type = message.text.strip().lower()
    payment_tokens = {
            '💳 click': CLICK_TOKEN,
            '💳 payme': PAYME_TOKEN
    }
    prices = [LabeledPrice(label="Telegram Premium Subscription", amount=100000)]
    try:
        set_user_state(user_id, UserStates.payment_type.state)
        await message.reply_invoice(
            title=f"Premium channel {payment_type.removeprefix('💳 ').upper()}",
            description="Premium kanalga kirish orqali marketingda maksimal imkoniyatlardan foydalaning.",
            payload=f"{payment_type.removeprefix('💳 ').upper()}",
            provider_token=payment_tokens.get(payment_type, CLICK_TOKEN),
            currency="UZS",
            prices=prices,
            start_parameter="premium_upgrade",
            reply_markup=purchase_button()
        )
        await state.set_state(UserStates.payment_type)   
    except Exception as e:
        await bot.send_message(ADMIN_ID, format_error("handle_payment", message, e))


@router.pre_checkout_query(lambda _: True)
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    except Exception as e:
        await bot.send_message(ADMIN_ID, format_error("pre-checkout", None, e, pre_checkout_query.id))

@router.message(lambda message: message.successful_payment is not None, StateFilter(UserStates.payment_type))
async def successful_payment_handler(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    try:
        total_price = message.successful_payment.total_amount / 100
        payment_type = message.successful_payment.invoice_payload
        generated_link = await generate_one_time_link(bot, LINK_CHANNEL_ID)
        payment_movement_id = add_to_payment_movements(
            message.from_user.id,
            generated_link,
            total_price,
            payment_type
        )
        set_user_state(user_id, UserStates.start.state)
        await bot.send_message(ADMINS_GROUP_ID, format_payment_success(message, total_price, payment_type, generated_link, payment_movement_id))
        await message.reply(get_translation('success_message').replace(':link',generated_link), parse_mode='HTML', reply_markup=main_menu_keyboard())
        await state.set_state(UserStates.start) 
    except Exception as e:
        await bot.send_message(ADMIN_ID, format_error("payment success", message, e))


@router.message(lambda message: message.text == GO_BACK, StateFilter(UserStates.payment_type))
async def handle_back(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    try:
        set_user_state(user_id, UserStates.warning.state)
        await message.reply(
            get_translation('warning_message'),
            reply_markup=confirmation_keyboard(),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.warning)   
    except Exception as e:
        await bot.send_message(ADMIN_ID, format_error("back", message, e))

@router.message(lambda message: message.text == DECLINE_JOIN, StateFilter(UserStates.warning))
async def handle_sure_not(message: Message, state: FSMContext, bot: Bot):
    
    user_id = message.from_user.id
    try:
        set_user_state(user_id, UserStates.start.state)
        await message.reply(
            get_translation('start_message'),
            reply_markup=main_menu_keyboard(),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.start)   
    except Exception as e:
        await bot.send_message(ADMIN_ID, format_error("sure_not", message, e))

@router.message(lambda message: message.text == BOOK_CONSULTATION, StateFilter(UserStates.start))
async def handle_consultation(message: Message, bot: Bot):
    try:
        await message.reply(
            get_translation('consultation_message'),
            reply_markup=main_menu_keyboard(),
            parse_mode='HTML'
        )
    except Exception as e:
        await bot.send_message(ADMIN_ID, format_error("consultation", message, e))

@router.message(lambda message: message.text == CONTACT_DEVELOPER, StateFilter(UserStates.start))
async def handle_consultation(message: Message):
    try:
        await message.reply(
            get_translation('it_service_message'),
            reply_markup=main_menu_keyboard(),
            parse_mode='HTML'
        )
    except Exception as e:
        pass

@router.message(lambda message: message.text == MARKETING_SERVICE, StateFilter(UserStates.start))
async def handle_smm(message: Message, bot: Bot):
    try:
        await message.reply(
            get_translation('smm_message'),
            reply_markup=main_menu_keyboard(),
            parse_mode='HTML'
        )
    except Exception as e:
        await bot.send_message(ADMIN_ID, format_error("SMM handler", message, e))
@router.message(lambda message: message.text == FREE_KNOWLEDGE, StateFilter(UserStates.start))
async def handle_free(message: Message, bot: Bot):
    try:
        send = await bot.copy_message(chat_id=message.chat.id, from_chat_id=SOURCE_CHANNEL_ID, message_id=PDF_MESSAGE_ID)
        await message.answer(get_translation('free_knowledge_full_message'), reply_to_message_id=send.message_id, parse_mode='HTML')
    except Exception as e:
        await bot.send_message(ADMIN_ID, format_error("FREE MESAGE handler", message, e))

@router.message(StateFilter(UserStates.start, UserStates.warning, UserStates.payment_type))
async def handle_unrecognized_input(message: Message, state: FSMContext):
    current_state = await state.get_state()
    state_responses = {
        UserStates.start: {
            "text": get_translation('start_message'),
            "keyboard": main_menu_keyboard()
        },
        UserStates.warning: {
            "text": get_translation('warning_message'), 
            "keyboard": confirmation_keyboard()
        },
        UserStates.payment_type: {
            "text": get_translation('payment_type_message'),  
            "keyboard": payment_options_keyboard()
        },
        UserStates.payment_success: {
            "text": get_translation('success_message').replace(':link', ''),  
            "keyboard": main_menu_keyboard()
        }
    }
    response = state_responses.get(current_state, {
        "text": get_translation('start_message'),
        "keyboard": main_menu_keyboard()
    })
    await message.reply(
        response["text"],
        reply_markup=response["keyboard"],
        parse_mode='HTML'
    )

@router.message()
async def fallback_handler(message: Message, state: FSMContext):
    await message.reply(get_translation('start_message'), parse_mode='HTML', reply_markup=main_menu_keyboard())
    await state.set_state(UserStates.start) 
