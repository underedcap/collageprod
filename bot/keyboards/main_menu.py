from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛡 Тарифы")],
            [KeyboardButton(text="💳 Купить VPN")],
            [KeyboardButton(text="📦 Мои заказы")],
        ],
        resize_keyboard=True
    )