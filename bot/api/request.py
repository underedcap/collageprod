import aiohttp
from bot.config import BACKEND_URL

async def create_user(telegram_id, username):
    data = {
        "telegramId": telegram_id,
        "username": username,
        "tariffName": "",
        "durationDays": 0
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BACKEND_URL}/api/users/subscribe", json=data) as resp:
                return True
    except Exception as e:
        print("Ошибка при создании пользователя:", e)
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
            async with session.post(f"{BACKEND_URL}/api/users/subscribe", json=data) as resp:
                if resp.status == 200:
                    return await resp.text()
    except Exception as e:
        print("Ошибка подписки:", e)
    return "❌ Ошибка подписки"

async def get_user_info(telegram_id):
    url = f"{BACKEND_URL}/api/users/{telegram_id}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
    except Exception as e:
        print("Ошибка при получении профиля:", e)
    return None