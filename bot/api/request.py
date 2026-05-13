import aiohttp
from config import BACKEND_URL


async def create_user(telegram_id, username):
    data = {
        "telegramId": telegram_id,
        "username": username,
        "tariffName": "",
        "durationDays": 0
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BACKEND_URL}/users/subscribe", json=data) as response:
                return True
    except Exception as e:
        print(e)
    return False


async def subscribe_user(telegram_id, username, tariff_name, duration_days):
    data = {
        "telegramId": telegram_id,
        "username": username,
        "tariffName": tariff_name,
        "durationDays": duration_days
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BACKEND_URL}/users/subscribe", json=data) as response:
                if response.status == 200:
                    return await response.text()
    except Exception as e:
        print(e)

    return "❌ Ошибка подписки"