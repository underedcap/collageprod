from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌍 VPN 8+ стран")],
            [KeyboardButton(text="🇷🇺 Белые списки РФ")],
        ],
        resize_keyboard=True
    )