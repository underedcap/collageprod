from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.main_menu import main_menu_kb
from request import create_user

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await create_user(message.from_user.id, message.from_user.username)

    await message.answer(
        "👋 Привет! Выбери тариф для VPN:",
        reply_markup=main_menu_kb()
    )