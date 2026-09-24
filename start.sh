#!/bin/bash
cd "$(dirname "$0")"
[ -d venv ] || python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
if [ ! -f .env ]; then
  cp .env.example .env
  echo ".env faylini to'ldiring (nano .env), so'ng qayta ishga tushiring."
  exit 1
fi
python bot.py
