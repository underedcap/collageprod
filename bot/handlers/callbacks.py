from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.texts.messages import OFFER_TEXT
from bot.texts.messages import PRIVACY_TEXT

router = Router()


@router.callback_query(F.data == "offer")
async def offer_handler(callback: CallbackQuery):

    await callback.answer()

    await callback.message.answer(
        OFFER_TEXT
    )


@router.callback_query(F.data == "privacy")
async def privacy_handler(callback: CallbackQuery):

    await callback.answer()

    await callback.message.answer(
        PRIVACY_TEXT
    )


@router.callback_query(F.data == "back")
async def back_handler(callback: CallbackQuery):

    await callback.message.delete()