"""
Render.com (va boshqa "web service" turidagi bepul xostinglar) uchun
webhook rejimida ishlaydigan bot.

Farqi bot.py dan: bot.py — VPS/server uchun (polling rejimi, doimiy
ishlaydigan kompyuterda). web_bot.py — Render kabi "web service" talab
qiladigan platformalar uchun (webhook rejimi, HTTP orqali ishlaydi).

Ishga tushirish (lokal test uchun ham mumkin):
    python web_bot.py
"""

import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from admin import router as admin_router
from config import BOT_TOKEN
from database import init_db
from handlers import router as handlers_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

WEBHOOK_PATH = "/webhook"
# Telegramdan kelayotgan so'rov haqiqiyligini tekshirish uchun maxfiy kalit
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "teatr-bot-maxfiy-kalit")
# Render avtomatik ravishda PORT o'zgaruvchisini beradi
PORT = int(os.getenv("PORT", 10000))
# Render avtomatik ravishda RENDER_EXTERNAL_URL beradi (masalan:
# https://teatr-bot.onrender.com). Boshqa platformada BASE_URL ni qo'lda
# kiritish kerak bo'lishi mumkin.
BASE_URL = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("BASE_URL")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(admin_router)
dp.include_router(handlers_router)


async def on_startup(app: web.Application) -> None:
    await init_db()
    if not BASE_URL:
        logger.warning(
            "❌ BASE_URL/RENDER_EXTERNAL_URL topilmadi — webhook o'rnatilmadi! "
            "Render muhitida bu avtomatik bo'lishi kerak."
        )
        return
    webhook_url = f"{BASE_URL}{WEBHOOK_PATH}"
    await bot.set_webhook(
        webhook_url, secret_token=WEBHOOK_SECRET, drop_pending_updates=True
    )
    logger.info("✅ Webhook o'rnatildi: %s", webhook_url)


async def on_shutdown(app: web.Application) -> None:
    await bot.delete_webhook()
    logger.info("Webhook o'chirildi.")


async def health(request: web.Request) -> web.Response:
    """UptimeRobot kabi xizmatlar shu manzilga so'rov yuborib, botni
    'uyg'oq' ushlab turadi (Render bepul tarifida uxlab qolmasligi uchun)."""
    return web.Response(text="OK — Teatr bot ishlayapti ✅")


def main() -> None:
    app = web.Application()
    app.router.add_get("/", health)

    SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET
    ).register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    logger.info("🚀 Web server %s portda ishga tushmoqda...", PORT)
    web.run_app(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
