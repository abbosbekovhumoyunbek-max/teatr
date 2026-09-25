"""
Yordamchi funksiyalar:
  - JSON fayllardan ma'lumot o'qish (xatolarga chidamli)
  - Xabarni xavfsiz tahrirlash (matn <-> rasm/video xabarlari orasida
    almashinganda Telegram xato bermasligi uchun)
"""

import json
import logging
import os
from typing import Any

from aiogram.types import InlineKeyboardMarkup, Message

from config import DATA_DIR

logger = logging.getLogger(__name__)


def _load_json(filename: str, default: Any) -> Any:
    """JSON faylni xavfsiz o'qiydi. Fayl topilmasa yoki buzilgan bo'lsa,
    dasturni to'xtatmasdan standart qiymatni qaytaradi."""
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Fayl topilmadi: %s", path)
        return default
    except json.JSONDecodeError as e:
        logger.error("JSON xatosi (%s): %s", filename, e)
        return default


def get_spectacles_from_file() -> list[dict]:
    return _load_json("spectacles.json", [])


def get_membership() -> list[dict]:
    return _load_json("membership.json", [])


def get_actors() -> list[dict]:
    return _load_json("actors.json", [])


def get_gallery_from_file() -> list[dict]:
    return _load_json("gallery.json", [])


def get_history() -> dict:
    return _load_json("history.json", {})


def get_trips() -> list[dict]:
    return _load_json("trips.json", [])


def get_news_from_file() -> list[dict]:
    return _load_json("news.json", [])


def get_faq() -> list[dict]:
    return _load_json("faq.json", [])


def get_contact() -> dict:
    return _load_json("contact.json", {})


def group_by_date(spectacles: list[dict]) -> dict[str, list[dict]]:
    """Spektakllarni sana bo'yicha guruhlaydi (haftalik jadval uchun),
    xronologik tartibda saralaydi."""
    grouped: dict[str, list[dict]] = {}
    for s in spectacles:
        date_key = s.get("date", "Nomaʼlum sana")
        grouped.setdefault(date_key, []).append(s)
    return dict(sorted(grouped.items()))


async def safe_edit(
    message: Message, text: str, markup: InlineKeyboardMarkup | None = None
) -> None:
    """Xabarni tahrirlashga harakat qiladi. Agar joriy xabar rasm/video
    bo'lsa (matn tahrirlab bo'lmaydi), eskisini o'chirib, yangi matnli
    xabar yuboradi. Shu tufayl bo'limlar orasida o'tishda xato chiqmaydi."""
    try:
        await message.edit_text(text, reply_markup=markup)
    except Exception:
        try:
            await message.delete()
        except Exception:
            pass
        await message.answer(text, reply_markup=markup)
