from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.keyboards.main_menu import main_menu_kb

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "👋 Привет! Выберите действие:",
        reply_markup=main_menu_kb()
    )