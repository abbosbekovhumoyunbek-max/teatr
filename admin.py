"""
Admin panel.

Faqat config.py dagi ADMIN_IDS ro'yxatida turgan Telegram foydalanuvchilar
uchun ishlaydi. /admin buyrug'i bilan ochiladi.

Imkoniyatlar:
  - Yangi spektakl qo'shish
  - Yangi yangilik/e'lon qo'shish
  - Barcha foydalanuvchilarga xabar yuborish (broadcast)
  - Statistika ko'rish (foydalanuvchilar soni va h.k.)
"""

import datetime
import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import database
import utils
from config import ADMIN_IDS

logger = logging.getLogger(__name__)
router = Router()


# ============================== YORDAMCHI FUNKSIYALAR ==============================

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


def admin_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="➕ Yangi spektakl qo'shish", callback_data="admin:add_spectacle")
    )
    builder.row(
        InlineKeyboardButton(text="🖼 Galereyaga rasm/video qo'shish", callback_data="admin:add_gallery")
    )
    builder.row(
        InlineKeyboardButton(text="📢 Yangilik qo'shish", callback_data="admin:add_news")
    )
    builder.row(
        InlineKeyboardButton(text="✉️ Barchaga xabar yuborish", callback_data="admin:broadcast")
    )
    builder.row(InlineKeyboardButton(text="📊 Statistika", callback_data="admin:stats"))
    return builder.as_markup()


def back_to_admin_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Admin menyu", callback_data="admin:menu"))
    return builder.as_markup()


# ============================== FSM HOLATLARI ==============================

class AddSpectacle(StatesGroup):
    title = State()
    genre = State()
    duration = State()
    date = State()
    time = State()
    description = State()
    photo = State()


class AddGallery(StatesGroup):
    media = State()
    caption = State()


class AddNews(StatesGroup):
    title = State()
    text = State()


class Broadcast(StatesGroup):
    text = State()
    confirm = State()


# ============================== ADMIN MENYU ==============================

@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext) -> None:
    if not is_admin(message.from_user.id):
        # Oddiy foydalanuvchiga bu buyruq umuman mavjud emasdek ko'rinadi
        return
    await state.clear()
    await message.answer("🔐 <b>Admin panel</b>\n\nNima qilmoqchisiz?", reply_markup=admin_menu_kb())


@router.callback_query(F.data == "admin:menu")
async def cb_admin_menu(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer()
        return
    await state.clear()
    await utils.safe_edit(
        callback.message, "🔐 <b>Admin panel</b>\n\nNima qilmoqchisiz?", admin_menu_kb()
    )
    await callback.answer()


# ============================== STATISTIKA ==============================

@router.callback_query(F.data == "admin:stats")
async def cb_stats(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer()
        return
    users = await database.get_users()
    spectacles = await database.get_spectacles()
    news = await database.get_news()
    text = (
        "📊 <b>Statistika</b>\n\n"
        f"👥 Botdan foydalanganlar: <b>{len(users)}</b> kishi\n"
        f"🎭 Spektakllar soni: {len(spectacles)}\n"
        f"🎨 Aktyorlar soni: {len(utils.get_actors())}\n"
        f"📢 Yangiliklar soni: {len(news)}\n"
        f"🧳 Sayohatlar soni: {len(utils.get_trips())}"
    )
    if not database.MONGODB_URI:
        text += "\n\n⚠️ MONGODB_URI sozlanmagan — yangi qo'shilgan ma'lumotlar saqlanmaydi!"
    await utils.safe_edit(callback.message, text, back_to_admin_kb())
    await callback.answer()


# ============================== YANGI SPEKTAKL QO'SHISH ==============================

@router.callback_query(F.data == "admin:add_spectacle")
async def cb_add_spectacle_start(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer()
        return
    await state.set_state(AddSpectacle.title)
    await utils.safe_edit(callback.message, "🎭 Spektakl nomini yozing:")
    await callback.answer()


@router.message(AddSpectacle.title)
async def add_spectacle_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(AddSpectacle.genre)
    await message.answer("🎬 Janrini yozing (masalan: Drama, Komediya):")


@router.message(AddSpectacle.genre)
async def add_spectacle_genre(message: Message, state: FSMContext) -> None:
    await state.update_data(genre=message.text)
    await state.set_state(AddSpectacle.duration)
    await message.answer("⏱ Davomiyligini yozing (masalan: 2 soat):")


@router.message(AddSpectacle.duration)
async def add_spectacle_duration(message: Message, state: FSMContext) -> None:
    await state.update_data(duration=message.text)
    await state.set_state(AddSpectacle.date)
    await message.answer("📅 Sanasini yozing (masalan: 2026-11-01):")


@router.message(AddSpectacle.date)
async def add_spectacle_date(message: Message, state: FSMContext) -> None:
    await state.update_data(date=message.text)
    await state.set_state(AddSpectacle.time)
    await message.answer("🕐 Vaqtini yozing (masalan: 18:00):")


@router.message(AddSpectacle.time)
async def add_spectacle_time(message: Message, state: FSMContext) -> None:
    await state.update_data(time=message.text)
    await state.set_state(AddSpectacle.description)
    await message.answer("📝 Qisqa tavsifini yozing:")


@router.message(AddSpectacle.description)
async def add_spectacle_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(AddSpectacle.photo)
    await message.answer(
        "🖼 Endi shu spektakl uchun rasm yuboring (talabalar shu rasmni ko'radi).\n"
        "Agar hozircha rasm bo'lmasa, \"yo'q\" deb yozing."
    )


@router.message(AddSpectacle.photo, F.photo)
async def add_spectacle_photo(message: Message, state: FSMContext) -> None:
    photo_file_id = message.photo[-1].file_id
    await _finish_add_spectacle(message, state, photo_file_id)


@router.message(AddSpectacle.photo)
async def add_spectacle_photo_skip(message: Message, state: FSMContext) -> None:
    # Foydalanuvchi rasm o'rniga matn yozsa (masalan "yo'q"), rasmsiz davom etamiz
    await _finish_add_spectacle(message, state, None)


async def _finish_add_spectacle(
    message: Message, state: FSMContext, photo_file_id: str | None
) -> None:
    data = await state.get_data()
    await state.clear()

    await database.add_spectacle(
        {
            "title": data["title"],
            "genre": data["genre"],
            "duration": data["duration"],
            "date": data["date"],
            "time": data["time"],
            "description": data["description"],
            "photo_file_id": photo_file_id,
        }
    )

    confirmation = f"✅ \"{data['title']}\" spektakli muvaffaqiyatli qo'shildi!"
    if photo_file_id:
        confirmation += " (rasm bilan birga)"
    await message.answer(confirmation, reply_markup=back_to_admin_kb())


# ============================== GALEREYAGA RASM/VIDEO QO'SHISH ==============================

@router.callback_query(F.data == "admin:add_gallery")
async def cb_add_gallery_start(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer()
        return
    await state.set_state(AddGallery.media)
    await utils.safe_edit(
        callback.message,
        "🖼 Galereyaga qo'shmoqchi bo'lgan rasm yoki videoni shu yerga yuboring:",
    )
    await callback.answer()


@router.message(AddGallery.media, F.photo)
async def add_gallery_photo(message: Message, state: FSMContext) -> None:
    await state.update_data(file_id=message.photo[-1].file_id, media_type="photo")
    await state.set_state(AddGallery.caption)
    await message.answer("📝 Endi shu rasm uchun qisqa izoh (caption) yozing:")


@router.message(AddGallery.media, F.video)
async def add_gallery_video(message: Message, state: FSMContext) -> None:
    await state.update_data(file_id=message.video.file_id, media_type="video")
    await state.set_state(AddGallery.caption)
    await message.answer("📝 Endi shu video uchun qisqa izoh (caption) yozing:")


@router.message(AddGallery.media)
async def add_gallery_invalid(message: Message) -> None:
    await message.answer("⚠️ Iltimos, matn emas — rasm yoki video yuboring.")


@router.message(AddGallery.caption)
async def add_gallery_caption(message: Message, state: FSMContext) -> None:
    data = await state.update_data(caption=message.text)
    await state.clear()

    await database.add_gallery_item(
        {
            "caption": data["caption"],
            "file_id": data["file_id"],
            "type": data["media_type"],
        }
    )

    await message.answer("✅ Galereyaga muvaffaqiyatli qo'shildi!", reply_markup=back_to_admin_kb())


# ============================== YANGI YANGILIK QO'SHISH ==============================

@router.callback_query(F.data == "admin:add_news")
async def cb_add_news_start(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer()
        return
    await state.set_state(AddNews.title)
    await utils.safe_edit(callback.message, "📢 Yangilik sarlavhasini yozing (masalan: '🔥 Yangi mavsum'):")
    await callback.answer()


@router.message(AddNews.title)
async def add_news_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(AddNews.text)
    await message.answer("📝 Yangilik matnini yozing:")


@router.message(AddNews.text)
async def add_news_text(message: Message, state: FSMContext) -> None:
    data = await state.update_data(text=message.text)
    await state.clear()

    await database.add_news_item(
        {
            "title": data["title"],
            "text": data["text"],
            "date": datetime.date.today().isoformat(),
            "image_file_id": None,
        }
    )

    await message.answer("✅ Yangilik muvaffaqiyatli qo'shildi!", reply_markup=back_to_admin_kb())


# ============================== BARCHAGA XABAR YUBORISH ==============================

@router.callback_query(F.data == "admin:broadcast")
async def cb_broadcast_start(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer()
        return
    await state.set_state(Broadcast.text)
    await utils.safe_edit(
        callback.message, "✉️ Barcha foydalanuvchilarga yuboriladigan xabar matnini yozing:"
    )
    await callback.answer()


@router.message(Broadcast.text)
async def broadcast_text(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    await state.set_state(Broadcast.confirm)
    users_count = len(await database.get_users())

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Ha, yuborish", callback_data="admin:broadcast_confirm"),
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin:menu"),
    )
    await message.answer(
        f"Quyidagi xabar <b>{users_count}</b> foydalanuvchiga yuboriladi:\n\n"
        f"—————————\n{message.text}\n—————————\n\nTasdiqlaysizmi?",
        reply_markup=builder.as_markup(),
    )


@router.callback_query(F.data == "admin:broadcast_confirm")
async def cb_broadcast_confirm(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer()
        return
    data = await state.get_data()
    text = data.get("text", "")
    await state.clear()

    users = await database.get_users()
    sent, failed = 0, 0
    await utils.safe_edit(callback.message, "⏳ Yuborilmoqda, biroz kuting...")

    for user_id in users:
        try:
            await callback.bot.send_message(user_id, f"📢 {text}")
            sent += 1
        except Exception as e:
            logger.warning("Xabar yuborilmadi (user_id=%s): %s", user_id, e)
            failed += 1

    await utils.safe_edit(
        callback.message,
        f"✅ Xabar yuborish yakunlandi!\n\n✔️ Muvaffaqiyatli: {sent}\n❌ Yetkazilmadi: {failed}",
        back_to_admin_kb(),
    )
    await callback.answer()
