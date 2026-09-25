"""
Bot konfiguratsiyasi.
Token va boshqa maxfiy ma'lumotlar .env faylidan o'qiladi (hech qachon
kod ichiga yozilmaydi — bu xavfsizlik uchun muhim).
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    sys.exit(
        "\n❌ XATOLIK: BOT_TOKEN topilmadi.\n\n"
        "Buni tuzatish uchun:\n"
        "  1) .env.example faylidan nusxa oling va nomini '.env' deb o'zgartiring\n"
        "     (Linux/Mac: cp .env.example .env)\n"
        "  2) .env faylini oching va BOT_TOKEN= qatoriga @BotFather dan\n"
        "     olingan tokeningizni yozing\n"
        "  3) Botni qayta ishga tushiring\n"
    )

# Ma'lumotlar (JSON fayllar) joylashgan papka
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Admin foydalanuvchilarning Telegram ID raqamlari (.env da vergul bilan ajratib yoziladi)
ADMIN_IDS = [
    int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()
]
