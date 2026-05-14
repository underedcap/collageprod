from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import text, bold, link

router = Router()

# Ссылки на политики
TERMS_URL = "https://t.me/InsightDlC_Vpn_bot"
REFUND_URL = "https://t.me/InsightDlC_Vpn_bot"
PRIVACY_URL = "https://t.me/InsightDlC_Vpn_bot"

# Ссылки на оплату
SBP_PAYMENT_URL = "https://your-sbp-link.com"  # вставь свою ссылку на оплату через СБП
CRYPTO_PAYMENT_URL = "https://t.me/YourCryptoWalletBot"  # Trust Wallet USDT TRC20

@router.message()
async def show_offer(message: Message):
    price = "149 ₽"

    msg_text = text(
        "Привет! Выберите тариф для оплаты:\n\n",
        bold("1 Месяц\n"),
        f"Стоимость: <b><i><u>{price}</u></i></b>\n\n",
        "Переходя к оплате, вы соглашаетесь с ",
        link("условиями использования", TERMS_URL), ", ",
        link("политикой возвратов", REFUND_URL), " и ",
        link("политикой конфиденциальности", PRIVACY_URL),
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить через СБП", url=SBP_PAYMENT_URL)],
        [InlineKeyboardButton(text="Оплатить Crypto (USDT TRC20)", url=CRYPTO_PAYMENT_URL)],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])

    await message.answer(msg_text, reply_markup=keyboard, parse_mode="HTML")