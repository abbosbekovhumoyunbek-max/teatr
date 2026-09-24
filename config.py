import os

# Bot tokenini @BotFather'dan oling va shu yerga yoki muhit o'zgaruvchisiga qo'ying
BOT_TOKEN = os.getenv("BOT_TOKEN", "PUT_YOUR_BOT_TOKEN_HERE")

# Admin bo'lishi kerak bo'lgan Telegram user ID'lar (vergul bilan ajratilgan)
# O'z ID'ingizni bilish uchun @userinfobot ga /start yozing
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "123456789").split(",") if x.strip()]

DB_PATH = "bot_database.db"
