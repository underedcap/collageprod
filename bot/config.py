import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:8080"
)
