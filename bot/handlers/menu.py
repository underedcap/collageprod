from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "🛡 Тарифы")
async def tariffs(message: Message):
    await message.answer("💰 Тарифы:\n- 1 месяц\n- 3 месяца\n- 12 месяцев")


@router.message(F.text == "💳 Купить VPN")
async def buy(message: Message):
    await message.answer("💳 Оплата пока в разработке")


@router.message(F.text == "📦 Мои заказы")
async def orders(message: Message):
    await message.answer("📦 У вас пока нет заказов")