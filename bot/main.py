from aiogram import Bot, Dispatcher
import asyncio

from config import BOT_TOKEN

from handlers.start import router as start_router


async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)

    print("BOT STARTED")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
