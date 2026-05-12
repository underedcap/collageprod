import asyncio
import os
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

from handlers.start import router as start_router
from handlers.menu import router as menu_router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)

    dp.include_router(start_router)
    dp.include_router(menu_router)

    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())