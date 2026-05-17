import aiohttp
from config import BACKEND_URL

BASE_URL = BACKEND_URL


async def get_user(telegram_id: int):

    async with aiohttp.ClientSession() as session:

        async with session.get(
                f"{BASE_URL}/api/users/{telegram_id}"
        ) as response:

            if response.status == 200:
                return await response.json()

            return None


async def activate_subscription(
        telegram_id: int,
        username: str,
        order_id: int | None = None
):

    payload = {
        "telegramId": telegram_id,
        "username": username,
        "tariffName": "1 Month",
        "durationDays": 30,
        "price": 149
    }

    if order_id is not None:
        payload["orderId"] = order_id

    async with aiohttp.ClientSession() as session:

        async with session.post(
                f"{BASE_URL}/api/users/subscribe",
                json=payload
        ) as response:

            if response.status >= 400:
                raise RuntimeError(await response.text())

            if response.content_type == "application/json":
                return await response.json()

            return {"status": await response.text()}


async def create_payment_order(
        telegram_id: int,
        username: str
):
    payload = {
        "telegramId": telegram_id,
        "username": username,
        "tariffName": "1 Month",
        "durationDays": 30,
        "price": 149
    }

    async with aiohttp.ClientSession() as session:

        async with session.post(
                f"{BASE_URL}/api/orders/create",
                json=payload
        ) as response:

            if response.status >= 400:
                raise RuntimeError(await response.text())

            return await response.json()
