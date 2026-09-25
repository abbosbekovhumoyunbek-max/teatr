"""
Teatr Telegram boti — asosiy ishga tushirish fayli.

Ishga tushirish:
    python bot.py

Talab qilinadigan narsalar:
    - .env faylida BOT_TOKEN (config.py va .env.example ga qarang)
    - requirements.txt dagi kutubxonalar o'rnatilgan bo'lishi kerak
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from admin import router as admin_router
from config import BOT_TOKEN
from database import init_db
from handlers import router as handlers_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    # Admin router BIRINCHI ulanishi kerak — aks holda handlers.py dagi
    # umumiy "fallback" xabar handleri admin buyruqlarini "ushlab qolishi" mumkin.
    dp.include_router(admin_router)
    dp.include_router(handlers_router)

    # Eski (ishlatilmagan) yangilanishlarni tashlab, tozadan boshlaymiz
    await bot.delete_webhook(drop_pending_updates=True)

    # MongoDB ulanishini tayyorlaymiz (bo'sh bo'lsa, namuna ma'lumot bilan to'ldiradi)
    await init_db()

    me = await bot.get_me()
    logger.info("✅ Bot ishga tushdi: @%s (%s)", me.username, me.full_name)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot to'xtatildi.")
