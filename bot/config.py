import os
BOT_TOKEN = os.getenv("BOT_TOKEN", "8161003048:AAEK1cwtPJuhDMy9-eTqzEoYIingBX2qcFc")

# BACKEND_URL: если задан в env, берём его; иначе fallback на localhost
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")

# Флаг режима
IS_LOCAL = "localhost" in BACKEND_URL

print(f"Запуск бота в {'локальном' if IS_LOCAL else 'контейнерном'} режиме")