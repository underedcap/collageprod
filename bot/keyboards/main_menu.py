from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧑 Профиль"), KeyboardButton(text="💳 Купить VPN")],
        ],
        resize_keyboard=True
    )

def vpn_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌍 VPN 8+ стран")],
            [KeyboardButton(text="🇷🇺 Белые списки РФ")],
            [KeyboardButton(text="⬅️ Назад")],
        ],
        resize_keyboard=True
    )