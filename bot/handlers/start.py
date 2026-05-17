from pathlib import Path

from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery, FSInputFile

from keyboards.inline import (
    main_menu_kb,
    buy_menu_kb,
    back_main_kb,
    close_policy_kb,
    profile_kb,
    payment_kb,
    OFFER_URL,
    REFUND_URL,
    PRIVACY_URL,
    PAYMENT_URL,
    CRYPTO_ADDRESS,
)
from api.backend import get_user, activate_subscription, create_payment_order
from terms.offer import PUBLIC_OFFER
from terms.privacy import PRIVACY_POLICY
from terms.refund import REFUND_POLICY

router = Router()
POLICY_MESSAGES: dict[int, list[int]] = {}

BANNER_PATHS = (
    Path(__file__).resolve().parent.parent / "assets" / "banner.jpg",
    Path(__file__).resolve().parent.parent / "assets" / "banner.png",
)
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

def banner_file() -> FSInputFile:
    for path in BANNER_PATHS:
        if path.exists():
            return FSInputFile(path)
    expected = ", ".join(str(path) for path in BANNER_PATHS)
    raise FileNotFoundError(f"Banner asset not found. Expected one of: {expected}")

@router.message(CommandStart(deep_link=True))
async def deep_links(message: Message, command: CommandObject):
    args = command.args
    if args == "offer":
        sent = await message.answer(PUBLIC_OFFER, reply_markup=close_policy_kb)
        POLICY_MESSAGES.setdefault(message.chat.id, []).append(sent.message_id)
        return
    if args == "refund":
        sent = await message.answer(REFUND_POLICY, reply_markup=close_policy_kb)
        POLICY_MESSAGES.setdefault(message.chat.id, []).append(sent.message_id)
        return
    if args == "privacy":
        sent = await message.answer(PRIVACY_POLICY, reply_markup=close_policy_kb)
        POLICY_MESSAGES.setdefault(message.chat.id, []).append(sent.message_id)
        return

    await start_handler(message)

@router.message(CommandStart())
async def start_handler(message: Message):
    banner = banner_file()
    
    await message.answer_photo(
        photo=banner,
        caption=WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=main_menu_kb
    )

@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):
    await callback.answer()
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
    await callback.message.answer(text, reply_markup=profile_kb, parse_mode="HTML")

@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await callback.answer()
    banner = banner_file()
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=banner,
        caption=WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=main_menu_kb
    )

@router.callback_query(F.data == "buy_vpn")
async def buy_vpn(callback: CallbackQuery):
    await callback.answer()
    caption = (
        "Вы выбрали: <b>1 Месяц</b>\n"
        "Стоимость: <b>149 ₽</b> <s>349 ₽</s>\n\n"
        "Переходя к оплате, вы соглашаетесь с "
        f'<a href="{OFFER_URL}">условиями пользования</a>, '
        f'<a href="{REFUND_URL}">политикой возвратов</a> и '
        f'<a href="{PRIVACY_URL}">политикой конфиденциальности</a>.'
    )

    if callback.message.caption is None:
        banner = banner_file()
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=banner,
            caption=caption,
            parse_mode="HTML",
            reply_markup=buy_menu_kb
        )
        return

    await callback.message.edit_caption(
        caption=caption,
        parse_mode="HTML",
        reply_markup=buy_menu_kb
    )

@router.callback_query(F.data == "policy_offer")
async def show_offer_policy(callback: CallbackQuery):
    await callback.answer()
    sent = await callback.message.answer(PUBLIC_OFFER, reply_markup=close_policy_kb)
    POLICY_MESSAGES.setdefault(callback.message.chat.id, []).append(sent.message_id)

@router.callback_query(F.data == "policy_refund")
async def show_refund_policy(callback: CallbackQuery):
    await callback.answer()
    sent = await callback.message.answer(REFUND_POLICY, reply_markup=close_policy_kb)
    POLICY_MESSAGES.setdefault(callback.message.chat.id, []).append(sent.message_id)

@router.callback_query(F.data == "policy_privacy")
async def show_privacy_policy(callback: CallbackQuery):
    await callback.answer()
    sent = await callback.message.answer(PRIVACY_POLICY, reply_markup=close_policy_kb)
    POLICY_MESSAGES.setdefault(callback.message.chat.id, []).append(sent.message_id)

@router.callback_query(F.data == "close_policy")
async def close_policy(callback: CallbackQuery):
    await callback.answer()
    chat_id = callback.message.chat.id
    message_ids = POLICY_MESSAGES.pop(chat_id, [])
    if callback.message.message_id not in message_ids:
        message_ids.append(callback.message.message_id)
    for message_id in message_ids:
        try:
            await callback.bot.delete_message(chat_id, message_id)
        except Exception:
            pass

@router.callback_query(F.data == "pay")
async def payment(callback: CallbackQuery):
    try:
        order = await create_payment_order(
            telegram_id=callback.from_user.id,
            username=callback.from_user.username or ""
        )
    except Exception:
        await callback.answer(
            "Не получилось создать счёт. Попробуйте позже или напишите в поддержку.",
            show_alert=True
        )
        return

    await callback.answer()
    order_id = order["orderId"]
    payment_url = order.get("paymentUrl", PAYMENT_URL)

    await callback.message.edit_caption(
        caption=(
            "💳 <b>Выберите способ оплаты</b>\n"
            f"Заказ: <code>{order_id}</code>\n\n"
            "Подписка: <b>1 Месяц</b>\n"
            "К оплате: <b>149 ₽</b>\n\n"
            "СБП: оплата по тестовой ссылке.\n"
            "CryptoBot / USDT TRC20: адрес кошелька откроется по кнопке.\n\n"
            "После оплаты нажмите <b>«Я оплатил»</b>."
        ),
        parse_mode="HTML",
        reply_markup=payment_kb(order_id, payment_url)
    )

@router.callback_query(F.data == "pay_crypto")
async def show_crypto_payment(callback: CallbackQuery):
    await callback.answer()
    caption = callback.message.caption or ""
    if CRYPTO_ADDRESS in caption:
        return

    await callback.message.edit_caption(
        caption=(
            f"{caption}\n\n"
            "CryptoBot / USDT TRC20:\n"
            f"<code>{CRYPTO_ADDRESS}</code>"
        ),
        parse_mode="HTML",
        reply_markup=callback.message.reply_markup
    )

@router.callback_query(F.data == "fake_success_payment")
@router.callback_query(F.data.startswith("fake_success_payment:"))
async def fake_payment(callback: CallbackQuery):
    order_id = None

    if ":" in callback.data:
        order_id = int(callback.data.split(":", 1)[1])

    try:
        result = await activate_subscription(
            telegram_id=callback.from_user.id,
            username=callback.from_user.username or "",
            order_id=order_id
        )
    except Exception:
        await callback.answer(
            "Не получилось активировать подписку. Попробуйте позже или напишите в поддержку.",
            show_alert=True
        )
        return

    await callback.answer()
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
