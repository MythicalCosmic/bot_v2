from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


FREE_KNOWLEDGE = "🎁 BEPUL BILIMLAR"
JOIN_PREMIUM_CHANNEL = "🌟 Yopiq kanalga qo'shilish"
MARKETING_SERVICE = "📣 Marketing xizmati"
CONTACT_DEVELOPER = "📞💻 Dasturchi bilan bog‘lanish"
CONFIRM_JOIN = "🚀 Kanalga qo'shilmoqchiman"
DECLINE_JOIN = "❌ Yo‘q, orqaga qaytish"
PURCHASE = "💰 Sotib olish"
GO_BACK = "🔙 Orqaga"
PAYMENT_CLICK = "💳 Click"
PAYMENT_PAYME = "💳 Payme"
BOOK_CONSULTATION = "💬 Konsultatsiyaga yozilish"
SPECIALIST_CONTACT = "💬 Mutaxasisga yozish"


URL = "https://telegram.me/getresult_uz"


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=FREE_KNOWLEDGE)],
            [KeyboardButton(text=JOIN_PREMIUM_CHANNEL), KeyboardButton(text=BOOK_CONSULTATION)],
            [KeyboardButton(text=CONTACT_DEVELOPER), KeyboardButton(text=MARKETING_SERVICE)]
        ],
        resize_keyboard=True
    )


def confirmation_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=CONFIRM_JOIN)],
            [KeyboardButton(text=DECLINE_JOIN)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def payment_options_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=PAYMENT_CLICK), KeyboardButton(text=PAYMENT_PAYME)],
            [KeyboardButton(text=GO_BACK)]
        ],
        resize_keyboard=True
    )


def purchase_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=PURCHASE, pay=True)]
        ]
    )


def back_button() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=GO_BACK)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def marketing_contact_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=SPECIALIST_CONTACT, url=URL)]
        ]
    )


def consultation_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BOOK_CONSULTATION, url=URL)]
        ]
    )
