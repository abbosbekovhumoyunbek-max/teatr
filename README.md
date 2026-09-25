# 🎭 Teatr Telegram Boti

Talabalar uchun mo'ljallangan teatr boti. Kino botlarga o'xshab tez va tugma
orqali ishlaydi, lekin sotib olish emas — **ma'lumot berish** uchun.

## Bo'limlar

- 🎭 Joriy spektakllar
- 📅 Haftalik jadval
- 🎫 Teatr a'zosi bo'lish
- 🎨 Aktyorlar profili
- 📸 Foto/video galereya
- 🏆 Teatr tarixi va yutuqlari
- 🧳 Sayohatlar / ekskursiyalar
- 📢 Yangiliklar va e'lonlar
- ❓ Ko'p so'raladigan savollar
- 📞 Bog'lanish

## Loyiha tuzilmasi

```
teatr_bot/
├── bot.py              # Botni ishga tushiruvchi asosiy fayl
├── config.py           # Sozlamalar (token, admin ID lar)
├── keyboards.py        # Barcha tugmalar (inline klaviaturalar)
├── handlers.py         # Har bir bo'lim uchun mantiq
├── utils.py             # JSON o'qish va yordamchi funksiyalar
├── data/                # BARCHA MATNLI MA'LUMOTLAR shu yerda (JSON)
│   ├── spectacles.json
│   ├── membership.json
│   ├── actors.json
│   ├── gallery.json
│   ├── history.json
│   ├── trips.json
│   ├── news.json
│   ├── faq.json
│   └── contact.json
├── requirements.txt
└── .env.example
```

**Muhim:** Kontentni (spektakllar, aktyorlar, yangiliklar va h.k.) o'zgartirish
uchun kodni tuzatish shart emas — shunchaki `data/` papkasidagi tegishli
`.json` faylni tahrirlang va botni qayta ishga tushiring.

## O'rnatish (birinchi marta)

### 1. Bot tokenini olish

1. Telegramda [@BotFather](https://t.me/BotFather) ga o'ting
2. `/newbot` buyrug'ini yuboring va ko'rsatmalarga amal qiling
3. Sizga token beriladi, masalan: `123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 2. Python muhitini tayyorlash

```bash
cd teatr_bot
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Tokenni sozlash

```bash
cp .env.example .env
```

`.env` faylini oching va shunday to'ldiring:

```
BOT_TOKEN=123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ADMIN_IDS=
```

### 4. Botni ishga tushirish

```bash
python bot.py
```

Konsolda `✅ Bot ishga tushdi: @sizning_botingiz` degan xabarni ko'rsangiz —
bot ishga tushdi. Endi Telegramda botingizni topib, `/start` bosing.

## 🔐 Admin panel

Botda o'z ichida ishlaydigan admin panel bor — alohida sayt yoki dastur kerak
emas, hammasi Telegramning o'zida.

### Nima qila oladi

- ➕ **Yangi spektakl qo'shish** — bot savol-javob tarzida so'raydi (nomi,
  janri, davomiyligi, sanasi, vaqti, tavsifi), so'ng **rasm yuborishni**
  so'raydi (yoki "yo'q" deb rasmsiz qoldirish mumkin) va avtomatik
  `data/spectacles.json` ga yozadi
- 🖼 **Galereyaga rasm/video qo'shish** — telefondagi/kompyuterdagi istalgan
  rasm yoki videoni to'g'ridan-to'g'ri botga yuborasiz, qisqa izoh
  yozasiz — tamom, `file_id`ni qo'lda izlash shart emas
- 📢 **Yangilik/e'lon qo'shish** — sarlavha va matn kiritasiz, avtomatik
  bugungi sana bilan `data/news.json` ga qo'shiladi
- ✉️ **Barchaga xabar yuborish (broadcast)** — botdan hech bo'lmaganda bir
  marta `/start` bosgan barcha foydalanuvchilarga bir vaqtda xabar yuboradi
- 📊 **Statistika** — foydalanuvchilar soni, spektakllar, aktyorlar,
  yangiliklar va sayohatlar sonini ko'rsatadi

### Bir nechta admin qo'shish (hammasiga bir xil huquq)

`.env` faylidagi `ADMIN_IDS` qatoriga bir nechta Telegram ID'ni vergul bilan
ajratib yozsangiz, ro'yxatdagi **barcha** shaxslar bir xil huquqqa ega
bo'ladi — har biri mustaqil ravishda spektakl qo'sha oladi, rasm yuklay
oladi, yangilik e'lon qila oladi va barchaga xabar yubora oladi:

```
ADMIN_IDS=123456789,987654321,555555555
```

Yangi admin qo'shish uchun: uning Telegram ID raqamini oling (u ham
@userinfobot orqali), shu qatorga vergul bilan qo'shing, botni qayta
ishga tushiring.

### Qanday yoqish kerak

1. O'zingizning Telegram ID raqamingizni bilib oling: Telegramda
   [@userinfobot](https://t.me/userinfobot) ga `/start` yuboring, u sizga
   ID raqamingizni ko'rsatadi (masalan: `123456789`)
2. `.env` faylini oching, `ADMIN_IDS=` qatoriga shu raqamni yozing:
   ```
   ADMIN_IDS=123456789
   ```
   Bir nechta admin bo'lsa, vergul bilan ajrating: `ADMIN_IDS=123456789,987654321`
3. Botni qayta ishga tushiring
4. Botga `/admin` buyrug'ini yuboring — admin panel ochiladi

**Muhim:** `ADMIN_IDS` ro'yxatida bo'lmagan har qanday foydalanuvchi
`/admin` buyrug'ini yuborsa, bot hech qanday javob bermaydi (xavfsizlik
uchun shunday qilingan — begonalar admin panel borligini ham bilmaydi).

## 🌐 Render.com orqali joylashtirish (VPS o'rniga)

Render.com kabi "web service" xostinglar VPS'dan farqli ishlaydi — kodni
zip fayl sifatida yuklab bo'lmaydi, u faqat **GitHub repozitoriyasidan**
o'qiydi. Shuning uchun avval kodni GitHub'ga joylashtirish kerak.

**Muhim:** Render bepul tarifida bot `web_bot.py` orqali (webhook rejimida)
ishlashi kerak, `bot.py` (polling) emas — aks holda 15 daqiqadan keyin
"uxlab qoladi".

### 1. Kodni GitHub'ga joylash

```bash
cd teatr_bot
git init
git add .
git commit -m "Teatr bot"
```

GitHub.com'da yangi bo'sh repozitoriya yarating (masalan `teatr-bot`), so'ng:

```bash
git remote add origin https://github.com/FOYDALANUVCHI_NOMI/teatr-bot.git
git branch -M main
git push -u origin main
```

### 2. Render'da Web Service yaratish

1. [render.com](https://render.com) ga kiring, **"New +"** → **"Web Service"**
2. GitHub repozitoriyangizni tanlang (`teatr-bot`)
3. Sozlamalar:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python web_bot.py`
   - **Instance Type:** Free
4. **Environment Variables** bo'limida qo'shing:
   - `BOT_TOKEN` = @BotFather'dan olgan tokeningiz
   - `ADMIN_IDS` = sizning Telegram ID raqamingiz
5. **"Create Web Service"** tugmasini bosing

Bir necha daqiqadan so'ng bot avtomatik ishga tushadi va o'ziga webhook
o'rnatadi (buni kod ichida `web_bot.py` avtomatik bajaradi). Sizga
`https://teatr-bot-xxxx.onrender.com` kabi manzil beriladi.

### 3. Botni "uxlab qolishdan" saqlash (juda muhim!)

Bepul tarifda 15 daqiqa faolsizlikdan keyin bot uxlaydi. Buning oldini olish
uchun bepul **UptimeRobot** xizmatidan foydalaning:

1. [uptimerobot.com](https://uptimerobot.com) da bepul ro'yxatdan o'ting
2. **"Add New Monitor"** → turi: **HTTP(s)**
3. URL: Render bergan manzilingiz (masalan `https://teatr-bot-xxxx.onrender.com`)
4. Tekshirish oralig'i: **5 daqiqa**
5. Saqlang

Shundan keyin UptimeRobot har 5 daqiqada botingizga "salom" berib turadi va
u doim uyg'oq turadi.

**Eslatma:** Bu usul VPS'dagi kabi 100% kafolatlangan emas — Render vaqti-
vaqti bilan texnik xizmat ko'rsatish uchun qayta ishga tushishi mumkin
(lekin `Restart=always` kabi bot avtomatik tiklanadi). Agar to'liq
kafolatlangan 24/7 ishlashni xohlasangiz, Oracle Cloud yoki Google Cloud
(haqiqiy VPS) ko'proq tavsiya etiladi.

## 🗄 MongoDB Atlas — doimiy saqlash (Render bilan ishlatish uchun SHART)

Render'ning bepul tarifida server diski vaqtinchalik, shuning uchun admin
panel orqali qo'shilgan spektakl, galereya rasmlari, yangiliklar va
foydalanuvchilar ro'yxati **MongoDB Atlas**'da (bepul, bulutli, hech qachon
o'chmaydigan) saqlanadi.

**Agar buni sozlamasangiz:** bot ishlayveradi, lekin `/admin` orqali
qo'shgan narsalaringiz keyingi `git push` yoki Render'ning avtomatik qayta
ishga tushishida yo'qolib qoladi.

### Sozlash qadamlari

1. [mongodb.com/cloud/atlas/register](https://www.mongodb.com/cloud/atlas/register)
   saytida bepul ro'yxatdan o'ting
2. **"Build a Database"** → **"M0 Free"** tarifini tanlang → yaqin regionni
   tanlang (masalan, Frankfurt) → **"Create"**
3. **Database user** yaratish so'raladi: username va parol o'ylab toping
   (parolni saqlab qo'ying!)
4. **Network Access** bo'limida **"Allow access from anywhere"**
   (0.0.0.0/0) ni tanlang — Render'ning IP manzili doim o'zgarib turadi,
   shuning uchun bu kerak
5. **"Connect"** → **"Drivers"** → ulanish manzilini (connection string)
   nusxalang, u shunga o'xshaydi:
   ```
   mongodb+srv://username:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. `<password>` o'rniga haqiqiy parolingizni yozing, va `.net/` dan keyin
   baza nomini qo'shing: `.net/teatr_bot?retryWrites=...`
7. Shu tayyor manzilni:
   - **Lokal test uchun:** `.env` fayliga `MONGODB_URI=...` qatoriga yozing
   - **Render uchun:** Render dashboard → sizning xizmatingiz →
     **Environment** → **"Add Environment Variable"** → Key: `MONGODB_URI`,
     Value: shu manzil

Botni qayta ishga tushirgach, konsolda **"✅ MongoDB ulanishi tayyor"**
degan yozuvni ko'rasiz — shu bilan barcha admin orqali qo'shilgan narsalar
endi DOIMIY saqlanadi.

## Kontentni yangilash

Har bir `data/*.json` fayl oddiy matn tahrirlovchida (Notepad, VS Code va h.k.)
ochiladi. Masalan, yangi spektakl qo'shish uchun `data/spectacles.json` ga
yangi element qo'shing:

```json
{
  "id": 4,
  "title": "Yangi spektakl nomi",
  "genre": "Drama",
  "duration": "2 soat",
  "date": "2026-11-01",
  "time": "18:00",
  "description": "Qisqa tavsif."
}
```

**Diqqat:** JSON formatida har bir elementdan keyin vergul (`,`) qo'yish,
lekin oxirgi elementdan keyin qo'ymaslik kerak. Faylni saqlagach, botni
qayta ishga tushiring (`Ctrl+C`, keyin `python bot.py`).

## Rasm/video qo'shish (aktyorlar, galereya, yangiliklar)

Telegram bot fayllarni to'g'ridan-to'g'ri emas, balki `file_id` orqali
yuboradi. Buni olish uchun eng oson yo'l:

1. Botga (yoki [@userinfobot](https://t.me/userinfobot) kabi yordamchi botga)
   kerakli rasmni yuboring
2. Konsolda yoki botning javobida chiqqan `file_id` qiymatini nusxalang
3. Uni tegishli JSON faylga qo'ying, masalan:

```json
"photo_file_id": "AgACAgIAAxkBAAI...."
```

Agar `file_id` bo'sh (`null`) qoldirilsa, bot avtomatik ravishda faqat
matnli xabar yuboradi — xatolik bermaydi.

## Botni doimiy ishlab turishi uchun (production)

Kompyuteringizni o'chirsangiz ham bot ishlashda davom etishi uchun uni
serverga (masalan, VPS) joylashtirish kerak. Eng oddiy variant:

```bash
# serverda
nohup python bot.py > bot.log 2>&1 &
```

Yoki `systemd`, `screen`, `tmux`, yoki Docker orqali ishga tushirish tavsiya
etiladi — bular loyihani kengaytirishda ko'proq barqarorlik beradi.

## Keyingi qadamlar (kelajakda qo'shish mumkin bo'lgan narsalar)

- 🔔 Admin panel orqali barcha foydalanuvchilarga push-xabar yuborish
- 🗳 Spektakllarga ovoz berish / reyting tizimi
- 🥇 "Eng faol tomoshabin" nishonlari (badge) tizimi
- 🤝 Do'stni taklif qilish (referal) tizimi
- 🗄 JSON fayllar o'rniga to'liq ma'lumotlar bazasi (PostgreSQL/SQLite)

Shu funksiyalardan birortasini qo'shishni xohlasangiz, ayting — birga
loyihalashtiramiz.
