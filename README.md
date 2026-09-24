# UZXIATeatrBot — Admin panelli video bot

## Nima qo'shildi
- `/admin` buyrug'i orqali ochiladigan admin panel (faqat `config.py` dagi `ADMIN_IDS` ro'yxatidagi userlar uchun)
- Kategoriyalar yaratish/o'chirish
- Video qo'shish (kategoriya tanlab, video yuborib, nom va tavsif kiritish orqali)
- Videoni tahrirlash: nomi, tavsifi, yoki videoning o'zini almashtirish
- Videoni o'chirish (tasdiqlash bilan)
- Oddiy foydalanuvchilar uchun: `/start` → kategoriya tanlash → video tanlash → video yuboriladi

## O'rnatish

1. Python 3.10+ o'rnatilgan bo'lishi kerak.
2. Kerakli kutubxonani o'rnating:
   ```
   pip install -r requirements.txt
   ```
3. `config.py` faylini oching:
   - `BOT_TOKEN` ga @BotFather'dan olingan tokeningizni qo'ying
   - `ADMIN_IDS` ga o'zingizning Telegram user ID'ingizni qo'ying (bir nechta bo'lsa vergul bilan: `123,456`)
     - ID'ingizni bilish uchun Telegram'da @userinfobot ga `/start` yozing

   Yoki muhit o'zgaruvchisi orqali ham berish mumkin:
   ```
   export BOT_TOKEN="123456:ABC..."
   export ADMIN_IDS="123456789,987654321"
   ```

4. Botni ishga tushiring:
   ```
   python3 bot.py
   ```

## Ishlatish

- Admin sifatida botga `/admin` yozing — admin panel ochiladi.
- Avval kamida bitta **kategoriya** yarating ("📁 Kategoriyalar" → "➕ Yangi kategoriya").
- Keyin "➕ Video qo'shish" orqali videolarni yuklang.
- Videolarni tahrirlash/o'chirish uchun "🎬 Videolarni boshqarish" bo'limidan foydalaning.
- Oddiy foydalanuvchilar botga `/start` yozganda kategoriyalarni va videolarni ko'radi.

## Eslatma

- Videolar sizning serveringizda saqlanmaydi — Telegram serverida saqlanadi, bot faqat `file_id` ni bazada saqlaydi (`bot_database.db`, SQLite). Shu sababli fayllar hajmi cheklovi yo'q, lekin bot boshqa tokendan foydalansa eski `file_id`'lar ishlamay qolishi mumkin.
- Botni doimiy ishlab turishi uchun serverga (VPS) joylashtirib, `systemd` yoki `screen`/`tmux` orqali fon jarayon sifatida ishga tushiring.
