from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import main_menu_kb

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "👋 Привет! Это hex vpn конфиги.",
        reply_markup=main_menu_kb()
    )