from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text

router = Router()

@router.message(Text(text="🛡 Тарифы"))
async def tariffs_handler(message: Message):
    await message.answer("Тарифы:\n1. Basic — 350 RUB\n2. Pro — 800 RUB")

@router.message(Text(text="💳 Купить VPN"))
async def buy_vpn_handler(message: Message):
    await message.answer("Выберите тариф:\n• Basic\n• Pro")

@router.message(Text(text="📦 Мои заказы"))
async def orders_handler(message: Message):
    await message.answer("У вас пока нет заказов")