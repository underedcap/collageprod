from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.texts.messages import SUPPORT_TEXT

router = Router()


@router.callback_query(F.data == "support")
async def support_handler(callback: CallbackQuery):

    await callback.message.edit_text(
        SUPPORT_TEXT
    )