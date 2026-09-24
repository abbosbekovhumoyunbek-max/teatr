from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# ---------- Admin asosiy menyu ----------

def admin_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="➕ Video qo'shish", callback_data="adm_add_video")
    kb.button(text="🎬 Videolarni boshqarish", callback_data="adm_manage_videos")
    kb.button(text="📁 Kategoriyalar", callback_data="adm_manage_categories")
    kb.adjust(1)
    return kb.as_markup()


def back_to_admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Admin menyuga qaytish", callback_data="adm_menu")
    return kb.as_markup()


def cancel_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="❌ Bekor qilish", callback_data="adm_cancel")
    return kb.as_markup()


# ---------- Kategoriyalar ----------

def categories_kb(categories, prefix: str, show_add: bool = False) -> InlineKeyboardMarkup:
    """prefix: 'catuser' (foydalanuvchi ko'rishi), 'catadmvideo' (video qo'shish/boshqarish uchun tanlash),
    'catadmmanage' (kategoriyani o'chirish uchun)"""
    kb = InlineKeyboardBuilder()
    for cat in categories:
        kb.button(text=cat["name"], callback_data=f"{prefix}:{cat['id']}")
    if show_add:
        kb.button(text="➕ Yangi kategoriya", callback_data="adm_add_category")
    kb.adjust(1)
    if prefix != "catuser":
        kb.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="adm_menu"))
    return kb.as_markup()


def category_manage_actions_kb(category_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🗑 Kategoriyani o'chirish", callback_data=f"adm_delcat:{category_id}")
    kb.button(text="⬅️ Orqaga", callback_data="adm_manage_categories")
    kb.adjust(1)
    return kb.as_markup()


def confirm_delete_category_kb(category_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Ha, o'chirish", callback_data=f"adm_delcat_yes:{category_id}")
    kb.button(text="❌ Yo'q", callback_data="adm_manage_categories")
    kb.adjust(1)
    return kb.as_markup()


# ---------- Videolar ----------

def videos_list_kb(videos, prefix: str) -> InlineKeyboardMarkup:
    """prefix: 'vidsee' (foydalanuvchi ko'rishi) yoki 'vidadm' (admin boshqarishi)"""
    kb = InlineKeyboardBuilder()
    for v in videos:
        kb.button(text=v["title"], callback_data=f"{prefix}:{v['id']}")
    kb.adjust(1)
    return kb.as_markup()


def video_actions_kb(video_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✏️ Nomini o'zgartirish", callback_data=f"adm_edittitle:{video_id}")
    kb.button(text="📝 Tavsifini o'zgartirish", callback_data=f"adm_editdesc:{video_id}")
    kb.button(text="🎞 Videoni almashtirish", callback_data=f"adm_editfile:{video_id}")
    kb.button(text="🗑 O'chirish", callback_data=f"adm_delvideo:{video_id}")
    kb.button(text="⬅️ Orqaga", callback_data="adm_manage_videos")
    kb.adjust(1)
    return kb.as_markup()


def confirm_delete_video_kb(video_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Ha, o'chirish", callback_data=f"adm_delvideo_yes:{video_id}")
    kb.button(text="❌ Yo'q", callback_data=f"vidadm:{video_id}")
    kb.adjust(1)
    return kb.as_markup()
