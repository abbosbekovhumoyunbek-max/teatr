from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

import database as db
import keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    categories = db.get_categories()
    if not categories:
        await message.answer("Hozircha hech qanday kategoriya qo'shilmagan. Keyinroq qayta urinib ko'ring.")
        return
    await message.answer(
        "Assalomu alaykum! O'zbek Xalq Ijodiyoti va Amaliy San'ati (yoki tegishli) teatr botiga xush kelibsiz.\n\n"
        "Quyidagi kategoriyalardan birini tanlang:",
        reply_markup=kb.categories_kb(categories, prefix="catuser"),
    )


@router.callback_query(F.data.startswith("catuser:"))
async def show_category_videos(callback: CallbackQuery):
    category_id = int(callback.data.split(":")[1])
    videos = db.get_videos_by_category(category_id)
    if not videos:
        await callback.answer("Bu kategoriyada hozircha video yo'q.", show_alert=True)
        return
    await callback.message.edit_text(
        "Kerakli videoni tanlang:",
        reply_markup=kb.videos_list_kb(videos, prefix="vidsee"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("vidsee:"))
async def send_video_to_user(callback: CallbackQuery):
    video_id = int(callback.data.split(":")[1])
    video = db.get_video(video_id)
    if not video:
        await callback.answer("Video topilmadi.", show_alert=True)
        return
    caption = video["title"]
    if video["description"]:
        caption += f"\n\n{video['description']}"
    await callback.message.answer_video(video=video["file_id"], caption=caption)
    await callback.answer()
