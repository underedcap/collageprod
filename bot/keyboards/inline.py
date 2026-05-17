from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

BOT_USERNAME = "InsightDlC_Vpn_bot"
BOT_URL = f"https://t.me/{BOT_USERNAME}"

OFFER_URL = f"{BOT_URL}?start=offer"
REFUND_URL = f"{BOT_URL}?start=refund"
PRIVACY_URL = f"{BOT_URL}?start=privacy"

PAYMENT_URL = "https://pay.example.com/insight-vpn-demo-149"
CRYPTO_ADDRESS = "TBPXP9ZUQW4bBgomeXVn41yfr8aTmcpqrv"

main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⚡ Купить подписку",
                callback_data="buy_vpn",
            )
        ],
        [
            InlineKeyboardButton(
                text="👤 Кабинет",
                callback_data="profile",
            ),
            InlineKeyboardButton(
                text="🛟 Поддержка",
                url="https://insightclient.tech/support",
            ),
        ],
    ]
)

buy_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Перейти к оплате",
                callback_data="pay",
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_main",
            )
        ],
    ]
)

profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⚡ Купить подписку",
                callback_data="buy_vpn",
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_main",
            )
        ],
    ]
)

def payment_kb(order_id: int, payment_url: str = PAYMENT_URL) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="СБП",
                url=payment_url,
            ),
            InlineKeyboardButton(
                text="CryptoBot / USDT",
                callback_data="pay_crypto",
            ),
        ],
        [
            InlineKeyboardButton(
                text="✅ Я оплатил",
                callback_data=f"fake_success_payment:{order_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_main",
            )
        ],
    ])

back_main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_main",
            )
        ],
    ]
)

close_policy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="close_policy",
            )
        ],
    ]
)
