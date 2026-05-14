import asyncio
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN, BACKEND_URL, IS_LOCAL
from bot.handlers.start import router as start_router
from bot.handlers.menu import router as menu_router

print(f"Используется бэкенд: {BACKEND_URL}")
print(f"Режим запуска: {'локальный' if IS_LOCAL else 'контейнерный'}")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(menu_router)

    print("BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())