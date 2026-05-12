from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def menu_handler(message: Message):

    text = message.text

    if text == "🛡 Тарифы":
        await message.answer(
            "Тарифы:\n"
            "1. Basic — 350 RUB\n"
            "2. Pro — 800 RUB"
        )

    elif text == "💳 Купить VPN":
        await message.answer(
            "Выберите тариф:\n"
            "• Basic\n"
            "• Pro"
        )

    elif text == "📦 Мои заказы":
        await message.answer(
            "У вас пока нет заказов"
        )