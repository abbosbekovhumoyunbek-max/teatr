import asyncio
import logging
import os

from aiohttp import web
from aiogram import Bot, Dispatcher, F
from dotenv import load_dotenv
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # arizalar shu ID ga keladi

# ---------- Tugma nomlari ----------
B_PLAYS = "🎭 Joriy spektakllar"
B_SCHEDULE = "📅 Haftalik jadval"
B_MEMBER = "🎫 Teatr a'zosi bo'lish"
B_ACTORS = "🎨 Aktyorlar profili"
B_GALLERY = "📸 Foto/video galereya"
B_HISTORY = "🏆 Teatr tarixi va yutuqlari"
B_TRIPS = "🧳 Teatr sayohatlari / ekskursiyalar"
B_NEWS = "📢 Yangiliklar va e'lonlar"
B_FAQ = "❓ Ko'p so'raladigan savollar"
B_CONTACT = "📞 Bog'lanish"
B_BACK = "⬅️ Asosiy menyu"

# ---------- Matnlar (o'zingiznikiga almashtiring) ----------
TEXTS = {
    B_PLAYS: "🎭 <b>Joriy spektakllar</b>\n\n1. «Spektakl nomi 1» — drama\n2. «Spektakl nomi 2» — komediya\n3. «Spektakl nomi 3» — bolalar uchun",
    B_SCHEDULE: "📅 <b>Haftalik jadval</b>\n\nDushanba — dam olish\nSeshanba — 18:00 «Spektakl 1»\nPayshanba — 18:00 «Spektakl 2»\nShanba — 17:00 «Spektakl 3»\nYakshanba — 16:00 «Spektakl 1»",
    B_ACTORS: "🎨 <b>Aktyorlar</b>\n\n• Ism Familiya — yetakchi aktyor\n• Ism Familiya — aktrisa\n• Ism Familiya — rejissyor",
    B_GALLERY: "📸 Galereya: https://t.me/sizning_kanalingiz\n📹 Video: https://youtube.com/@sizning_kanalingiz",
    B_HISTORY: "🏆 <b>Teatr tarixi</b>\n\nTeatr XXXX-yilda tashkil etilgan.\n\n<b>Yutuqlar:</b>\n• Respublika festivali g'olibi\n• Xalqaro festival diplomi",
    B_NEWS: "📢 <b>Yangiliklar</b>\n\nEng so'nggi e'lonlar kanalimizda: https://t.me/sizning_kanalingiz",
    B_FAQ: "❓ <b>Ko'p so'raladigan savollar</b>\n\n<b>Chipta narxi qancha?</b>\n50 000 so'mdan.\n\n<b>Bolalar uchun bormi?</b>\nHa, shanba kunlari.\n\n<b>Chiptani qayerdan olaman?</b>\nKassadan yoki bot orqali.",
    B_CONTACT: "📞 <b>Bog'lanish</b>\n\nTelefon: +998 XX XXX XX XX\nManzil: Toshkent, ...\nIsh vaqti: 10:00–19:00\nTelegram: @sizning_admin",
}

# ---------- Sayohatlar bo'limi ----------
T_BACKSTAGE = "🎬 Sahna ortiga ekskursiya"
T_WARDROBE = "👗 Kostyum va dekoratsiya ombori"
T_CITIES = "🚌 Boshqa shaharlardagi teatrlarga safar"
T_FEST = "🎪 Teatr festivallariga borish"

TRIPS = {
    T_BACKSTAGE: "🎬 <b>Sahna ortiga ekskursiya</b>\nSahna, grim xonasi va yoritish pultini ko'rasiz. Davomiyligi: 1 soat.",
    T_WARDROBE: "👗 <b>Kostyum va dekoratsiya omboriga tashrif</b>\nSpektakl kostyumlari va dekoratsiyalari bilan tanishasiz.",
    T_CITIES: "🚌 <b>Guruh safarlari</b>\nBoshqa shaharlardagi teatrlarga guruh bilan safar. Sanalar e'lon qilinadi.",
    T_FEST: "🎪 <b>Teatr festivallari</b>\nFestivallarga birgalikda boramiz. Ro'yxatga yozilish uchun admin bilan bog'laning.",
}


# ---------- Klaviaturalar ----------
def main_menu() -> ReplyKeyboardMarkup:
    rows = [
        [B_PLAYS, B_SCHEDULE],
        [B_MEMBER, B_ACTORS],
        [B_GALLERY, B_HISTORY],
        [B_TRIPS],
        [B_NEWS, B_FAQ],
        [B_CONTACT],
    ]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t) for t in row] for row in rows],
        resize_keyboard=True,
    )


def trips_menu() -> ReplyKeyboardMarkup:
    rows = [[T_BACKSTAGE], [T_WARDROBE], [T_CITIES], [T_FEST], [B_BACK]]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t) for t in row] for row in rows],
        resize_keyboard=True,
    )


def phone_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


# ---------- A'zo bo'lish (ariza) ----------
class Member(StatesGroup):
    name = State()
    phone = State()


dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}! 🎭\n"
        "Teatrimiz botiga xush kelibsiz. Bo'limni tanlang:",
        reply_markup=main_menu(),
    )


@dp.message(F.text == B_BACK)
async def back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Asosiy menyu:", reply_markup=main_menu())


@dp.message(F.text == B_MEMBER)
async def member_start(message: Message, state: FSMContext):
    await state.set_state(Member.name)
    await message.answer(
        "🎫 A'zo bo'lish uchun ariza.\nIsm-familiyangizni yozing:",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(Member.name, F.text)
async def member_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Member.phone)
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=phone_kb())


@dp.message(Member.phone)
async def member_phone(message: Message, state: FSMContext, bot: Bot):
    phone = message.contact.phone_number if message.contact else message.text
    data = await state.get_data()
    await state.clear()
    await message.answer(
        "✅ Arizangiz qabul qilindi! Tez orada siz bilan bog'lanamiz.",
        reply_markup=main_menu(),
    )
    if ADMIN_ID:
        await bot.send_message(
            ADMIN_ID,
            f"🎫 Yangi a'zolik arizasi\n👤 {data['name']}\n📞 {phone}\n"
            f"🔗 @{message.from_user.username or 'username yo‘q'}",
        )


@dp.message(F.text == B_TRIPS)
async def trips(message: Message):
    await message.answer(
        "🧳 <b>Teatr sayohatlari va ekskursiyalar</b>\nQaysi biri qiziq?",
        parse_mode="HTML",
        reply_markup=trips_menu(),
    )


@dp.message(F.text.in_(TRIPS.keys()))
async def trip_detail(message: Message):
    await message.answer(TRIPS[message.text], parse_mode="HTML")


@dp.message(F.text.in_(TEXTS.keys()))
async def section(message: Message):
    await message.answer(TEXTS[message.text], parse_mode="HTML")


@dp.message()
async def fallback(message: Message):
    await message.answer("Iltimos, menyudagi tugmalardan foydalaning 👇", reply_markup=main_menu())


async def health(request):
    return web.Response(text="OK")


async def start_web():
    # Render Web Service uchun: PORT ni tinglab turadi (bot uxlab qolmasligi uchun ham kerak)
    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_get("/health", health)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", "10000"))
    await web.TCPSite(runner, "0.0.0.0", port).start()


async def main():
    logging.basicConfig(level=logging.INFO)
    if not TOKEN:
        raise SystemExit("BOT_TOKEN topilmadi! Avval tokenni o'rnating.")
    await start_web()
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
