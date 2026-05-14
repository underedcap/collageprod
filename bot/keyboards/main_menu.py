from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⚡ Купить подписку",
                callback_data="buy"
            )
        ],
        [
            InlineKeyboardButton(
                text="👑 Кабинет",
                callback_data="profile"
            )
        ],
        [
            InlineKeyboardButton(
                text="🛠 Поддержка",
                callback_data="support"
            )
        ]
    ]
)