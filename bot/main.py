from aiogram import Bot, Dispatcher
import asyncio

from bot.config import BOT_TOKEN

from bot.handlers.start import router as start_router
from bot.handlers.buy import router as buy_router
from bot.handlers.support import router as support_router
from bot.handlers.callbacks import router as callbacks_router


async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(buy_router)
    dp.include_router(support_router)
    dp.include_router(callbacks_router)

    print("BOT STARTED")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())