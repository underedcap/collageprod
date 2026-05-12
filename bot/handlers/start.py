from aiogram import Router
from aiogram.types import Message
from keyboards.main_menu import main_menu_kb

router = Router()

@router.message(commands=["start"])
async def start_cmd(message: Message):
    await message.answer(
        "Привет 👋\nВыбери действие:",
        reply_markup=main_menu_kb()
    )