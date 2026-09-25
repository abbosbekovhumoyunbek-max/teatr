"""Botning barcha inline klaviaturalari (tugmalari) shu yerda joylashgan."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

MAIN_MENU_BUTTONS: list[tuple[str, str]] = [
    ("🎭 Joriy spektakllar", "menu:spectacles"),
    ("📅 Haftalik jadval", "menu:schedule"),
    ("🎫 Teatr a'zosi bo'lish", "menu:membership"),
    ("🎨 Aktyorlar profili", "menu:actors"),
    ("📸 Foto/video galereya", "menu:gallery"),
    ("🏆 Teatr tarixi va yutuqlari", "menu:history"),
    ("🧳 Sayohatlar / ekskursiyalar", "menu:trips"),
    ("📢 Yangiliklar va e'lonlar", "menu:news"),
    ("❓ Ko'p so'raladigan savollar", "menu:faq"),
    ("📞 Bog'lanish", "menu:contact"),
]


def main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for text, data in MAIN_MENU_BUTTONS:
        builder.row(InlineKeyboardButton(text=text, callback_data=data))
    return builder.as_markup()


def back_kb(target: str = "menu:main") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Bosh menyu", callback_data=target))
    return builder.as_markup()


def list_nav_kb(prefix: str, index: int, total: int) -> InlineKeyboardMarkup:
    """Ro'yxat elementlari (spektakl, aktyor, galereya, sayohat, yangilik)
    orasida oldinga/orqaga o'tish tugmalarini yaratadi."""
    builder = InlineKeyboardBuilder()
    row: list[InlineKeyboardButton] = []
    if index > 0:
        row.append(
            InlineKeyboardButton(text="⬅️", callback_data=f"{prefix}:{index - 1}")
        )
    row.append(InlineKeyboardButton(text=f"{index + 1}/{total}", callback_data="noop"))
    if index < total - 1:
        row.append(
            InlineKeyboardButton(text="➡️", callback_data=f"{prefix}:{index + 1}")
        )
    builder.row(*row)
    builder.row(InlineKeyboardButton(text="⬅️ Bosh menyu", callback_data="menu:main"))
    return builder.as_markup()
