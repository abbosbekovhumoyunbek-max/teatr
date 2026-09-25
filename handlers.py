"""
Botning barcha handler (ishlov beruvchi) funksiyalari shu yerda.
Har bir bo'lim uchun: ro'yxatni ko'rsatish + elementlar orasida navigatsiya.
"""

import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

import keyboards as kb
import utils
from database import register_user, get_spectacles, get_gallery, get_news

logger = logging.getLogger(__name__)
router = Router()


# ============================== START / BOSH MENYU ==============================

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await register_user(message.from_user.id)
    text = (
        "🎭 <b>Assalomu alaykum!</b>\n\n"
        "Bu — teatrimizning rasmiy botiga xush kelibsiz.\n"
        "Bu yerda siz spektakllar jadvali, aktyorlar, yangiliklar va boshqa "
        "ko'plab ma'lumotlarni topa olasiz.\n\n"
        "Quyidagi bo'limlardan birini tanlang 👇"
    )
    await message.answer(text, reply_markup=kb.main_menu_kb())


@router.callback_query(F.data == "menu:main")
async def cb_main_menu(callback: CallbackQuery) -> None:
    text = "🎭 <b>Bosh menyu</b>\n\nQuyidagi bo'limlardan birini tanlang 👇"
    await utils.safe_edit(callback.message, text, kb.main_menu_kb())
    await callback.answer()


@router.callback_query(F.data == "noop")
async def cb_noop(callback: CallbackQuery) -> None:
    """Sahifa raqami tugmasi — bosilganda hech narsa qilmaydi."""
    await callback.answer()


# ============================== JORIY SPEKTAKLLAR ==============================

def _format_spectacle(s: dict) -> str:
    return (
        f"🎭 <b>{s.get('title', 'Nomaʼlum')}</b>\n\n"
        f"🎬 Janr: {s.get('genre', '—')}\n"
        f"⏱ Davomiyligi: {s.get('duration', '—')}\n"
        f"📅 Sana: {s.get('date', '—')}\n"
        f"🕐 Vaqt: {s.get('time', '—')}\n\n"
        f"📝 {s.get('description', '')}"
    )


async def _show_spectacle(callback: CallbackQuery, index: int) -> None:
    spectacles = await get_spectacles()
    if not spectacles:
        await utils.safe_edit(
            callback.message,
            "🎭 Hozircha spektakllar ro'yxati bo'sh. Tez orada yangilanadi!",
            kb.back_kb(),
        )
        await callback.answer()
        return
    index = max(0, min(index, len(spectacles) - 1))
    spectacle = spectacles[index]
    text = _format_spectacle(spectacle)
    markup = kb.list_nav_kb("spectacle", index, len(spectacles))
    photo = spectacle.get("photo_file_id")

    try:
        await callback.message.delete()
    except Exception:
        pass

    if photo:
        await callback.message.answer_photo(photo, caption=text, reply_markup=markup)
    else:
        await callback.message.answer(text, reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == "menu:spectacles")
async def cb_spectacles(callback: CallbackQuery) -> None:
    await _show_spectacle(callback, 0)


@router.callback_query(F.data.startswith("spectacle:"))
async def cb_spectacle_nav(callback: CallbackQuery) -> None:
    index = int(callback.data.split(":")[1])
    await _show_spectacle(callback, index)


# ============================== HAFTALIK JADVAL ==============================

@router.callback_query(F.data == "menu:schedule")
async def cb_schedule(callback: CallbackQuery) -> None:
    spectacles = await get_spectacles()
    if not spectacles:
        await utils.safe_edit(
            callback.message, "📅 Hozircha jadval mavjud emas.", kb.back_kb()
        )
        await callback.answer()
        return
    grouped = utils.group_by_date(spectacles)
    lines = ["📅 <b>Haftalik jadval</b>"]
    for date, items in grouped.items():
        lines.append(f"\n📌 <b>{date}</b>")
        for s in items:
            lines.append(f"   • {s.get('time', '—')} — {s.get('title', '—')}")
    await utils.safe_edit(callback.message, "\n".join(lines), kb.back_kb())
    await callback.answer()


# ============================== TEATR A'ZOSI BO'LISH ==============================

@router.callback_query(F.data == "menu:membership")
async def cb_membership(callback: CallbackQuery) -> None:
    tiers = utils.get_membership()
    if not tiers:
        await utils.safe_edit(
            callback.message,
            "🎫 A'zolik haqida ma'lumot tez orada qo'shiladi.",
            kb.back_kb(),
        )
        await callback.answer()
        return
    lines = ["🎫 <b>Teatr a'zosi bo'ling!</b>"]
    for t in tiers:
        lines.append(f"\n🔹 <b>{t.get('name', '—')}</b> — {t.get('price', '—')}")
        for benefit in t.get("benefits", []):
            lines.append(f"   ✅ {benefit}")
        if t.get("how_to_join"):
            lines.append(f"   📝 {t['how_to_join']}")
    await utils.safe_edit(callback.message, "\n".join(lines), kb.back_kb())
    await callback.answer()


# ============================== AKTYORLAR PROFILI ==============================

def _format_actor(a: dict) -> str:
    roles = ", ".join(a.get("roles", [])) or "—"
    return (
        f"🎨 <b>{a.get('name', 'Nomaʼlum')}</b>\n\n"
        f"📖 {a.get('bio', '')}\n\n"
        f"🎭 O'ynagan rollari: {roles}"
    )


async def _show_actor(callback: CallbackQuery, index: int) -> None:
    actors = utils.get_actors()
    if not actors:
        await utils.safe_edit(
            callback.message, "🎨 Aktyorlar ro'yxati hali qo'shilmagan.", kb.back_kb()
        )
        await callback.answer()
        return
    index = max(0, min(index, len(actors) - 1))
    actor = actors[index]
    text = _format_actor(actor)
    markup = kb.list_nav_kb("actor", index, len(actors))
    photo = actor.get("photo_file_id")

    try:
        await callback.message.delete()
    except Exception:
        pass

    if photo:
        await callback.message.answer_photo(photo, caption=text, reply_markup=markup)
    else:
        await callback.message.answer(text, reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == "menu:actors")
async def cb_actors(callback: CallbackQuery) -> None:
    await _show_actor(callback, 0)


@router.callback_query(F.data.startswith("actor:"))
async def cb_actor_nav(callback: CallbackQuery) -> None:
    index = int(callback.data.split(":")[1])
    await _show_actor(callback, index)


# ============================== FOTO/VIDEO GALEREYA ==============================

async def _show_gallery(callback: CallbackQuery, index: int) -> None:
    items = await get_gallery()
    if not items:
        await utils.safe_edit(
            callback.message,
            "📸 Galereya hali bo'sh. Tez orada rasm va videolar qo'shiladi!",
            kb.back_kb(),
        )
        await callback.answer()
        return
    index = max(0, min(index, len(items) - 1))
    item = items[index]
    caption = f"📸 {item.get('caption', '')}"
    markup = kb.list_nav_kb("gallery", index, len(items))
    file_id = item.get("file_id")
    media_type = item.get("type", "photo")

    try:
        await callback.message.delete()
    except Exception:
        pass

    if file_id and media_type == "video":
        await callback.message.answer_video(file_id, caption=caption, reply_markup=markup)
    elif file_id:
        await callback.message.answer_photo(file_id, caption=caption, reply_markup=markup)
    else:
        await callback.message.answer(caption, reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == "menu:gallery")
async def cb_gallery(callback: CallbackQuery) -> None:
    await _show_gallery(callback, 0)


@router.callback_query(F.data.startswith("gallery:"))
async def cb_gallery_nav(callback: CallbackQuery) -> None:
    index = int(callback.data.split(":")[1])
    await _show_gallery(callback, index)


# ============================== TEATR TARIXI ==============================

@router.callback_query(F.data == "menu:history")
async def cb_history(callback: CallbackQuery) -> None:
    data = utils.get_history()
    body = data.get("text") if isinstance(data, dict) else None
    if not body:
        text = "🏆 Teatr tarixi haqida ma'lumot tez orada qo'shiladi."
    else:
        text = f"🏆 <b>Teatr tarixi va yutuqlari</b>\n\n{body}"
    await utils.safe_edit(callback.message, text, kb.back_kb())
    await callback.answer()


# ============================== SAYOHATLAR / EKSKURSIYALAR ==============================

def _format_trip(t: dict) -> str:
    return (
        f"🧳 <b>{t.get('title', 'Nomaʼlum')}</b>\n\n"
        f"📅 Sana: {t.get('date', '—')}\n"
        f"💵 Narxi: {t.get('price', '—')}\n"
        f"👥 O'rinlar soni: {t.get('seats', '—')}"
    )


async def _show_trip(callback: CallbackQuery, index: int) -> None:
    trips = utils.get_trips()
    if not trips:
        await utils.safe_edit(
            callback.message,
            "🧳 Hozircha rejalashtirilgan sayohatlar yo'q. Tez orada e'lon qilinadi!",
            kb.back_kb(),
        )
        await callback.answer()
        return
    index = max(0, min(index, len(trips) - 1))
    text = _format_trip(trips[index])
    await utils.safe_edit(
        callback.message, text, kb.list_nav_kb("trip", index, len(trips))
    )
    await callback.answer()


@router.callback_query(F.data == "menu:trips")
async def cb_trips(callback: CallbackQuery) -> None:
    await _show_trip(callback, 0)


@router.callback_query(F.data.startswith("trip:"))
async def cb_trip_nav(callback: CallbackQuery) -> None:
    index = int(callback.data.split(":")[1])
    await _show_trip(callback, index)


# ============================== YANGILIKLAR VA E'LONLAR ==============================

def _format_news(n: dict) -> str:
    return (
        f"📢 <b>{n.get('title', 'Nomaʼlum')}</b>\n\n"
        f"{n.get('text', '')}\n\n"
        f"🗓 {n.get('date', '')}"
    )


async def _show_news(callback: CallbackQuery, index: int) -> None:
    items = await get_news()
    if not items:
        await utils.safe_edit(
            callback.message, "📢 Hozircha yangiliklar yo'q.", kb.back_kb()
        )
        await callback.answer()
        return
    index = max(0, min(index, len(items) - 1))
    item = items[index]
    text = _format_news(item)
    markup = kb.list_nav_kb("news", index, len(items))
    image = item.get("image_file_id")

    try:
        await callback.message.delete()
    except Exception:
        pass

    if image:
        await callback.message.answer_photo(image, caption=text, reply_markup=markup)
    else:
        await callback.message.answer(text, reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == "menu:news")
async def cb_news(callback: CallbackQuery) -> None:
    await _show_news(callback, 0)


@router.callback_query(F.data.startswith("news:"))
async def cb_news_nav(callback: CallbackQuery) -> None:
    index = int(callback.data.split(":")[1])
    await _show_news(callback, index)


# ============================== KO'P SO'RALADIGAN SAVOLLAR ==============================

@router.callback_query(F.data == "menu:faq")
async def cb_faq(callback: CallbackQuery) -> None:
    faqs = utils.get_faq()
    if not faqs:
        await utils.safe_edit(
            callback.message, "❓ Savol-javoblar tez orada qo'shiladi.", kb.back_kb()
        )
        await callback.answer()
        return
    lines = ["❓ <b>Ko'p so'raladigan savollar</b>"]
    for item in faqs:
        lines.append(f"\n▪️ <b>{item.get('question', '')}</b>")
        lines.append(item.get("answer", ""))
    await utils.safe_edit(callback.message, "\n".join(lines), kb.back_kb())
    await callback.answer()


# ============================== BOG'LANISH ==============================

@router.callback_query(F.data == "menu:contact")
async def cb_contact(callback: CallbackQuery) -> None:
    c = utils.get_contact()
    text = (
        "📞 <b>Biz bilan bog'laning</b>\n\n"
        f"☎️ Telefon: {c.get('phone', '—')}\n"
        f"📲 Telegram: {c.get('telegram', '—')}\n"
        f"📷 Instagram: {c.get('instagram', '—')}\n"
        f"📍 Manzil: {c.get('address', '—')}"
    )
    await utils.safe_edit(callback.message, text, kb.back_kb())
    await callback.answer()


# ============================== NOMA'LUM XABARLAR ==============================

@router.message()
async def fallback_message(message: Message) -> None:
    """Foydalanuvchi tugma orqali emas, oddiy matn yozsa shu ishlaydi."""
    await message.answer(
        "Tushunmadim 🤔 Iltimos, quyidagi tugmalardan foydalaning:",
        reply_markup=kb.main_menu_kb(),
    )
