from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery, FSInputFile

from keyboards.inline import (
    main_menu_kb,
    buy_menu_kb,
    back_main_kb,
    payment_kb,
    OFFER_URL,
    REFUND_URL,
    PRIVACY_URL,
    PAYMENT_URL,
)
from api.backend import get_user, activate_subscription
from terms.offer import PUBLIC_OFFER
from terms.privacy import PRIVACY_POLICY
from terms.refund import REFUND_POLICY

router = Router()

WELCOME_TEXT = "Привет! Возвращаемся в нормальный интернет без цензуры?"

CABINET_TEXT_NO_SUB = (
    "💼 Кабинет\n\n"
    "⭐ Подписка: <b>не активна</b>\n\n"
    "💸 Кэшбэк: 0₽"
)

CABINET_TEXT_ACTIVE = (
    "💼 Кабинет\n\n"
    "⭐ Подписка: <b>активна</b>\n"
    "📅 До: {date}\n\n"
    "💸 Кэшбэк: 0₽"
)

@router.message(CommandStart(deep_link=True))
async def deep_links(message: Message, command: CommandObject):
    args = command.args
    if args == "offer":
        await message.answer(PUBLIC_OFFER, reply_markup=back_main_kb)
        return
    if args == "refund":
        await message.answer(REFUND_POLICY, reply_markup=back_main_kb)
        return
    if args == "privacy":
        await message.answer(PRIVACY_POLICY, reply_markup=back_main_kb)
        return

    await start_handler(message)

@router.message(CommandStart())
async def start_handler(message: Message):
    banner = FSInputFile("assets/banner.jpg")
    
    await message.answer_photo(
        photo=banner,
        caption=WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=main_menu_kb
    )

@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):
    user = await get_user(callback.from_user.id)
    if user and user.get("activeSubscription"):
        text = (
            f"💼 Кабинет\n\n"
            f"⭐ Подписка: <b>активна</b>\n"
            f"📅 До: {user.get('subscriptionEnd')}\n\n"
            f"💸 Кэшбэк: {user.get('cashback')}₽"
        )
    else:
        text = CABINET_TEXT_NO_SUB
    await callback.message.answer(text, reply_markup=back_main_kb, parse_mode="HTML")

@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    banner = FSInputFile("assets/banner.jpg")
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=banner,
        caption=WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=main_menu_kb
    )

@router.callback_query(F.data == "buy_vpn")
async def buy_vpn(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=(
            "Вы выбрали: <b>1 Месяц</b>\n"
            "Стоимость: <b><tg-spoiler>149 ₽</tg-spoiler></b> <s>349 ₽</s>\n\n"
            "Переходя к оплате, вы соглашаетесь с "
            f'<a href="{OFFER_URL}">условиями пользования</a>, '
            f'<a href="{REFUND_URL}">политикой возвратов</a> и '
            f'<a href="{PRIVACY_URL}">политикой конфиденциальности</a>.'
        ),
        parse_mode="HTML",
        reply_markup=buy_menu_kb
    )

@router.callback_query(F.data == "pay")
async def payment(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=(
            "🌍 Счёт на оплату создан.\n"
            "Подписка: 1 Месяц\n"
            "Стоимость: 149 ₽\n\n"
            f"Ссылка на оплату:\n{PAYMENT_URL}\n\n"
            "После оплаты нажмите кнопку «Я оплатил»."
        ),
        reply_markup=payment_kb
    )

@router.callback_query(F.data == "fake_success_payment")
async def fake_payment(callback: CallbackQuery):
    try:
        result = await activate_subscription(
            telegram_id=callback.from_user.id,
            username=callback.from_user.username or ""
        )
    except Exception:
        await callback.answer(
            "Не получилось активировать подписку. Попробуйте позже или напишите в поддержку.",
            show_alert=True
        )
        return

    subscription_end = result.get("subscriptionEnd", "30 дней")

    await callback.message.edit_caption(
        caption=(
            "✅ Подписка успешно активирована.\n"
            f"📅 Активна до: <b>{subscription_end}</b>\n\n"
            "Добро пожаловать в InsightVPN."
        ),
        parse_mode="HTML",
        reply_markup=back_main_kb
    )
