from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

purchase_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Оплатить",
                callback_data="pay"
            )
        ],
        [
            InlineKeyboardButton(
                text="📄 Оферта",
                callback_data="offer"
            ),
            InlineKeyboardButton(
                text="🔒 Privacy",
                callback_data="privacy"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="back"
            )
        ]
    ]
)