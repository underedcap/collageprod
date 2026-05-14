from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.terms.offer import PUBLIC_OFFER
from bot.terms.privacy import PRIVACY_POLICY

router = Router()

@router.callback_query(F.data == "show_terms")
async def show_terms(callback: CallbackQuery):

    text = (
        "📄 Политика и условия использования\n\n"
        f"{PUBLIC_OFFER}\n\n"
        f"{PRIVACY_POLICY}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=None
    )