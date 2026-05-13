import aiohttp
from config import BACKEND_URL


async def get_tariffs():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BACKEND_URL}/tariffs") as response:
                if response.status == 200:
                    return await response.json()
    except Exception as e:
        print(e)

    return []


async def create_order(telegram_id, tariff_name):
    data = {
        "telegramId": telegram_id,
        "tariffName": tariff_name
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{BACKEND_URL}/orders/create",
                json=data
            ) as response:
                if response.status == 200:
                    return "✅ Заказ создан"
    except Exception as e:
        print(e)

    return "❌ Ошибка создания заказа"


async def get_user_orders(telegram_id):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{BACKEND_URL}/orders/user/{telegram_id}"
            ) as response:
                if response.status == 200:
                    return await response.json()
    except Exception as e:
        print(e)

    return []