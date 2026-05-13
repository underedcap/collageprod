from aiogram import Router, F
from aiogram.types import Message
from request import subscribe_user

router = Router()


@router.message(F.text == "🌍 VPN 8+ стран")
async def vpn_8plus(message: Message):
    link = await subscribe_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        tariff_name="VPN 8+ стран",
        duration_days=30
    )
    await message.answer(f"🌍 Ссылка на оплату VPN 8+ стран:\n🔗 {link}")


@router.message(F.text == "🇷🇺 Белые списки РФ")
async def vpn_white_russia(message: Message):
    link = await subscribe_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        tariff_name="Белые списки РФ",
        duration_days=30
    )
    await message.answer(f"🇷🇺 Ссылка на оплату Белые списки РФ:\n🔗 {link}")