import aiohttp

from bot.config import BACKEND_URL


async def get_profile(telegram_id: int):

    async with aiohttp.ClientSession() as session:

        async with session.get(
            f"{BACKEND_URL}/api/users/{telegram_id}"
        ) as response:

            if response.status == 200:
                return await response.json()

            return None


async def activate_subscription(
        telegram_id: int,
        username: str
):

    payload = {
        "telegramId": telegram_id,
        "username": username,
        "tariffName": "1 Month",
        "durationDays": 30
    }

    async with aiohttp.ClientSession() as session:

        async with session.post(
            f"{BACKEND_URL}/api/users/subscribe",
            json=payload
        ) as response:

            return await response.text()