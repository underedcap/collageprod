from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

BOT_USERNAME = "InsightDlC_Vpn_bot"
BOT_URL = f"https://t.me/{BOT_USERNAME}"

OFFER_URL = f"{BOT_URL}?start=offer"
REFUND_URL = f"{BOT_URL}?start=refund"
PRIVACY_URL = f"{BOT_URL}?start=privacy"

PAYMENT_URL = "https://pay.example.com/insight-vpn-demo-149"

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
                text="Оферта",
                url=OFFER_URL
            ),
            InlineKeyboardButton(
                text="Возврат",
                url=REFUND_URL
            ),
            InlineKeyboardButton(
                text="Privacy",
                url=PRIVACY_URL
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
                url=PAYMENT_URL
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Я оплатил",
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
