from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⚡ Купить подписку",
                callback_data="buy_vpn"
            )
        ],
        [
            InlineKeyboardButton(
                text="👤 Кабинет",
                callback_data="profile"
            ),
            InlineKeyboardButton(
                text="🛟 Поддержка",
                url="https://insightclient.tech/support"
            )
        ]
    ]
)

buy_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Согласен, оплатить",
                callback_data="pay"
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_main"
            )
        ]
    ]
)

payment_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Перейти к оплате",
                callback_data="fake_success_payment"
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_main"
            )
        ]
    ]
)

back_main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_main"
            )
        ]
    ]
)

policy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_main"
            )
        ]
    ]
)