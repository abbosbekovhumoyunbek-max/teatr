from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import database as db
import keyboards as kb
from config import ADMIN_IDS
from states import AddCategory, AddVideo, EditVideo

router = Router()
router.message.filter(F.from_user.id.in_(ADMIN_IDS))
router.callback_query.filter(F.from_user.id.in_(ADMIN_IDS))


# ---------- Asosiy menyu ----------

@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🔧 Admin panel", reply_markup=kb.admin_menu_kb())


@router.callback_query(F.data == "adm_menu")
async def admin_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("🔧 Admin panel", reply_markup=kb.admin_menu_kb())
    await callback.answer()


@router.callback_query(F.data == "adm_cancel")
async def admin_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Bekor qilindi.\n\n🔧 Admin panel", reply_markup=kb.admin_menu_kb())
    await callback.answer()


# ---------- Kategoriyalarni boshqarish ----------

@router.callback_query(F.data == "adm_manage_categories")
async def manage_categories(callback: CallbackQuery):
    categories = db.get_categories()
    await callback.message.edit_text(
        "📁 Kategoriyalar. Ko'rish/o'chirish uchun tanlang, yoki yangi qo'shing:",
        reply_markup=kb.categories_kb(categories, prefix="catadmmanage", show_add=True),
    )
    await callback.answer()


@router.callback_query(F.data == "adm_add_category")
async def add_category_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddCategory.waiting_name)
    await callback.message.edit_text(
        "Yangi kategoriya nomini yuboring:", reply_markup=kb.cancel_kb()
    )
    await callback.answer()


@router.message(AddCategory.waiting_name)
async def add_category_finish(message: Message, state: FSMContext):
    db.add_category(message.text.strip())
    await state.clear()
    await message.answer(f"✅ Kategoriya qo'shildi: {message.text.strip()}", reply_markup=kb.back_to_admin_kb())


@router.callback_query(F.data.startswith("catadmmanage:"))
async def category_manage_actions(callback: CallbackQuery):
    category_id = int(callback.data.split(":")[1])
    category = db.get_category(category_id)
    if not category:
        await callback.answer("Kategoriya topilmadi.", show_alert=True)
        return
    videos_count = len(db.get_videos_by_category(category_id))
    await callback.message.edit_text(
        f"📁 {category['name']}\nIchida {videos_count} ta video bor.",
        reply_markup=kb.category_manage_actions_kb(category_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("adm_delcat:"))
async def delete_category_confirm(callback: CallbackQuery):
    category_id = int(callback.data.split(":")[1])
    await callback.message.edit_text(
        "⚠️ Bu kategoriya ichidagi barcha videolar ham o'chib ketadi. Rostdan o'chirilsinmi?",
        reply_markup=kb.confirm_delete_category_kb(category_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("adm_delcat_yes:"))
async def delete_category_finish(callback: CallbackQuery):
    category_id = int(callback.data.split(":")[1])
    db.delete_category(category_id)
    await callback.answer("O'chirildi.", show_alert=True)
    categories = db.get_categories()
    await callback.message.edit_text(
        "📁 Kategoriyalar:",
        reply_markup=kb.categories_kb(categories, prefix="catadmmanage", show_add=True),
    )


# ---------- Video qo'shish ----------

@router.callback_query(F.data == "adm_add_video")
async def add_video_choose_category(callback: CallbackQuery, state: FSMContext):
    categories = db.get_categories()
    if not categories:
        await callback.answer("Avval kamida bitta kategoriya yarating.", show_alert=True)
        return
    await state.set_state(AddVideo.choosing_category)
    await callback.message.edit_text(
        "Video qaysi kategoriyaga tegishli?",
        reply_markup=kb.categories_kb(categories, prefix="catadmvideo"),
    )
    await callback.answer()


@router.callback_query(AddVideo.choosing_category, F.data.startswith("catadmvideo:"))
async def add_video_choose_category_done(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split(":")[1])
    await state.update_data(category_id=category_id)
    await state.set_state(AddVideo.waiting_video)
    await callback.message.edit_text(
        "Endi video faylni shu yerga yuboring:", reply_markup=kb.cancel_kb()
    )
    await callback.answer()


@router.message(AddVideo.waiting_video, F.video)
async def add_video_receive_file(message: Message, state: FSMContext):
    await state.update_data(file_id=message.video.file_id)
    await state.set_state(AddVideo.waiting_title)
    await message.answer("Video nomini (sarlavhasini) yuboring:", reply_markup=kb.cancel_kb())


@router.message(AddVideo.waiting_video)
async def add_video_wrong_type(message: Message):
    await message.answer("Iltimos, video fayl yuboring (rasm yoki matn emas).")


@router.message(AddVideo.waiting_title)
async def add_video_receive_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AddVideo.waiting_description)
    await message.answer(
        "Video uchun tavsif yuboring (yoki o'tkazib yuborish uchun /skip yozing):",
        reply_markup=kb.cancel_kb(),
    )


@router.message(AddVideo.waiting_description, Command("skip"))
async def add_video_skip_description(message: Message, state: FSMContext):
    await _finish_add_video(message, state, description="")


@router.message(AddVideo.waiting_description)
async def add_video_receive_description(message: Message, state: FSMContext):
    await _finish_add_video(message, state, description=message.text.strip())


async def _finish_add_video(message: Message, state: FSMContext, description: str):
    data = await state.get_data()
    db.add_video(
        category_id=data["category_id"],
        file_id=data["file_id"],
        title=data["title"],
        description=description,
    )
    await state.clear()
    await message.answer(f"✅ Video qo'shildi: {data['title']}", reply_markup=kb.back_to_admin_kb())


# ---------- Videolarni boshqarish (tahrirlash/o'chirish) ----------

@router.callback_query(F.data == "adm_manage_videos")
async def manage_videos_choose_category(callback: CallbackQuery):
    categories = db.get_categories()
    if not categories:
        await callback.answer("Hech qanday kategoriya yo'q.", show_alert=True)
        return
    await callback.message.edit_text(
        "Qaysi kategoriyadagi videolarni boshqaramiz?",
        reply_markup=kb.categories_kb(categories, prefix="catadmmvid"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("catadmmvid:"))
async def manage_videos_list(callback: CallbackQuery):
    category_id = int(callback.data.split(":")[1])
    videos = db.get_videos_by_category(category_id)
    if not videos:
        await callback.answer("Bu kategoriyada video yo'q.", show_alert=True)
        return
    await callback.message.edit_text(
        "Tahrirlash/o'chirish uchun videoni tanlang:",
        reply_markup=kb.videos_list_kb(videos, prefix="vidadm"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("vidadm:"))
async def video_actions(callback: CallbackQuery):
    video_id = int(callback.data.split(":")[1])
    video = db.get_video(video_id)
    if not video:
        await callback.answer("Video topilmadi.", show_alert=True)
        return
    text = f"🎬 {video['title']}"
    if video["description"]:
        text += f"\n{video['description']}"
    await callback.message.edit_text(text, reply_markup=kb.video_actions_kb(video_id))
    await callback.answer()


# --- Nomini o'zgartirish ---

@router.callback_query(F.data.startswith("adm_edittitle:"))
async def edit_title_start(callback: CallbackQuery, state: FSMContext):
    video_id = int(callback.data.split(":")[1])
    await state.update_data(video_id=video_id)
    await state.set_state(EditVideo.waiting_new_title)
    await callback.message.edit_text("Yangi nomni yuboring:", reply_markup=kb.cancel_kb())
    await callback.answer()


@router.message(EditVideo.waiting_new_title)
async def edit_title_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    db.update_video_title(data["video_id"], message.text.strip())
    await state.clear()
    await message.answer("✅ Nomi yangilandi.", reply_markup=kb.back_to_admin_kb())


# --- Tavsifini o'zgartirish ---

@router.callback_query(F.data.startswith("adm_editdesc:"))
async def edit_desc_start(callback: CallbackQuery, state: FSMContext):
    video_id = int(callback.data.split(":")[1])
    await state.update_data(video_id=video_id)
    await state.set_state(EditVideo.waiting_new_description)
    await callback.message.edit_text("Yangi tavsifni yuboring:", reply_markup=kb.cancel_kb())
    await callback.answer()


@router.message(EditVideo.waiting_new_description)
async def edit_desc_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    db.update_video_description(data["video_id"], message.text.strip())
    await state.clear()
    await message.answer("✅ Tavsif yangilandi.", reply_markup=kb.back_to_admin_kb())


# --- Videoni almashtirish ---

@router.callback_query(F.data.startswith("adm_editfile:"))
async def edit_file_start(callback: CallbackQuery, state: FSMContext):
    video_id = int(callback.data.split(":")[1])
    await state.update_data(video_id=video_id)
    await state.set_state(EditVideo.waiting_new_file)
    await callback.message.edit_text("Yangi video faylni yuboring:", reply_markup=kb.cancel_kb())
    await callback.answer()


@router.message(EditVideo.waiting_new_file, F.video)
async def edit_file_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    db.update_video_file(data["video_id"], message.video.file_id)
    await state.clear()
    await message.answer("✅ Video fayl yangilandi.", reply_markup=kb.back_to_admin_kb())


@router.message(EditVideo.waiting_new_file)
async def edit_file_wrong_type(message: Message):
    await message.answer("Iltimos, video fayl yuboring.")


# --- O'chirish ---

@router.callback_query(F.data.startswith("adm_delvideo:"))
async def delete_video_confirm(callback: CallbackQuery):
    video_id = int(callback.data.split(":")[1])
    await callback.message.edit_text(
        "⚠️ Rostdan bu videoni o'chirmoqchimisiz?",
        reply_markup=kb.confirm_delete_video_kb(video_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("adm_delvideo_yes:"))
async def delete_video_finish(callback: CallbackQuery):
    video_id = int(callback.data.split(":")[1])
    db.delete_video(video_id)
    await callback.answer("O'chirildi.", show_alert=True)
    await callback.message.edit_text("🔧 Admin panel", reply_markup=kb.admin_menu_kb())
