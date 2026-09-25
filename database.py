"""
MongoDB orqali DOIMIY (persistent) ma'lumotlar saqlash.

NEGA KERAK: Render.com kabi bepul "web service" xostinglarda serverning
diski VAQTINCHALIK — har safar qayta deploy bo'lganda yoki server qayta
ishga tushganda, diskka yozilgan o'zgarishlar yo'qoladi. Shu sababli
/admin orqali qo'shilgan spektakllar, galereya, yangiliklar va
foydalanuvchilar ro'yxati endi shu yerda — MongoDB Atlas'da (bepul,
bulutli) saqlanadi. U hech qanday deploy yoki qayta ishga tushish bilan
o'chib ketmaydi.

Statik kontent (aktyorlar, teatr tarixi, FAQ, aloqa, a'zolik turlari,
sayohatlar) hamon oddiy data/*.json fayllarida qoladi — chunki ular admin
panel orqali emas, kodni GitHub'ga push qilish orqali tahrirlanadi, shuning
uchun ularga vaqtinchalik disk muammosi tegishli emas.

Agar .env faylida MONGODB_URI ko'rsatilmagan bo'lsa, bot baribir ishlaydi,
lekin admin panel orqali qo'shilgan narsalar qayta deploy'da yo'qoladi —
konsolda shu haqda ogohlantirish chiqadi.
"""

import logging
import os

from motor.motor_asyncio import AsyncIOMotorClient

import utils

logger = logging.getLogger(__name__)

MONGODB_URI = os.getenv("MONGODB_URI")
_client = None
_db = None


def _get_db():
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(MONGODB_URI)
        _db = _client.get_default_database(default="teatr_bot")
    return _db


async def _seed_if_empty(collection_name: str, seed_data: list[dict]) -> None:
    """Kolleksiya bo'sh bo'lsa (bot birinchi marta ishga tushganda), uni
    data/*.json dagi namuna yozuvlar bilan to'ldiradi."""
    db = _get_db()
    collection = db[collection_name]
    count = await collection.count_documents({})
    if count == 0 and seed_data:
        await collection.insert_many([dict(item) for item in seed_data])
        logger.info(
            "'%s' kolleksiyasi %d ta namuna yozuv bilan to'ldirildi.",
            collection_name,
            len(seed_data),
        )


async def init_db() -> None:
    """Bot ishga tushganda BIR MARTA chaqiriladi."""
    if not MONGODB_URI:
        logger.warning(
            "⚠️  MONGODB_URI topilmadi — spektakl/galereya/yangilik/"
            "foydalanuvchi ma'lumotlari DOIMIY saqlanmaydi! "
            ".env fayliga MongoDB ulanish manzilini qo'shing."
        )
        return
    await _seed_if_empty("spectacles", utils.get_spectacles_from_file())
    await _seed_if_empty("gallery", utils.get_gallery_from_file())
    await _seed_if_empty("news", utils.get_news_from_file())
    logger.info("✅ MongoDB ulanishi tayyor.")


async def _next_id(collection) -> int:
    last = await collection.find().sort("id", -1).limit(1).to_list(length=1)
    return (last[0]["id"] + 1) if last else 1


# ============================== SPEKTAKLLAR ==============================

async def get_spectacles() -> list[dict]:
    if not MONGODB_URI:
        return utils.get_spectacles_from_file()
    docs = await _get_db().spectacles.find({}, {"_id": 0}).sort("id", 1).to_list(length=None)
    return docs


async def add_spectacle(spectacle: dict) -> None:
    if not MONGODB_URI:
        raise RuntimeError("MONGODB_URI sozlanmagan — spektakl saqlab bo'lmaydi.")
    db = _get_db()
    spectacle["id"] = await _next_id(db.spectacles)
    await db.spectacles.insert_one(spectacle)


# ============================== GALEREYA ==============================

async def get_gallery() -> list[dict]:
    if not MONGODB_URI:
        return utils.get_gallery_from_file()
    docs = await _get_db().gallery.find({}, {"_id": 0}).sort("id", 1).to_list(length=None)
    return docs


async def add_gallery_item(item: dict) -> None:
    if not MONGODB_URI:
        raise RuntimeError("MONGODB_URI sozlanmagan — galereyaga saqlab bo'lmaydi.")
    db = _get_db()
    item["id"] = await _next_id(db.gallery)
    await db.gallery.insert_one(item)


# ============================== YANGILIKLAR ==============================

async def get_news() -> list[dict]:
    if not MONGODB_URI:
        return utils.get_news_from_file()
    docs = await _get_db().news.find({}, {"_id": 0}).sort("id", -1).to_list(length=None)
    return docs


async def add_news_item(item: dict) -> None:
    if not MONGODB_URI:
        raise RuntimeError("MONGODB_URI sozlanmagan — yangilik saqlab bo'lmaydi.")
    db = _get_db()
    item["id"] = await _next_id(db.news)
    await db.news.insert_one(item)


# ============================== FOYDALANUVCHILAR (broadcast uchun) ==============================

async def register_user(user_id: int) -> None:
    if not MONGODB_URI:
        return
    db = _get_db()
    await db.users.update_one(
        {"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True
    )


async def get_users() -> list[int]:
    if not MONGODB_URI:
        return []
    docs = await _get_db().users.find({}, {"_id": 0, "user_id": 1}).to_list(length=None)
    return [d["user_id"] for d in docs]
