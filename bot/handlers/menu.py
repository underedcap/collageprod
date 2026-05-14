from aiogram import Router, F
from aiogram.types import Message
from bot.api.request import subscribe_user, get_user_info
from bot.keyboards.main_menu import main_menu_kb, vpn_menu_kb

router = Router()

# Главное меню
@router.message(F.text == "💳 Купить VPN")
async def show_vpn_menu(message: Message):
    await message.answer(
        "Выберите тариф VPN:",
        reply_markup=vpn_menu_kb()
    )

@router.message(F.text == "🧑 Профиль")
async def show_profile(message: Message):
    tg_id = message.from_user.id
    user = await get_user_info(tg_id)

    if user:
        username = user.get("username", "Неизвестно")
        active = user.get("activeSubscription", False)
        subscription_end = user.get("subscriptionEnd", "—")

        text = (
            f"👤 Профиль пользователя:\n"
            f"Telegram ID: {tg_id}\n"
            f"Username: @{username}\n"
            f"Подписка: {'активна' if active else 'нет'}\n"
            f"Активна до: {subscription_end if active else '—'}"
        )
    else:
        text = "❌ Не удалось получить данные профиля"

    await message.answer(text, reply_markup=main_menu_kb())

# VPN подменю
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

@router.message(F.text == "⬅️ Назад")
async def back_to_main(message: Message):
    await message.answer(
        "Главное меню:",
        reply_markup=main_menu_kb()
    )