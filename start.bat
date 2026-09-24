@echo off
cd /d %~dp0
if not exist venv python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
if exist .env goto run
copy .env.example .env
echo .env faylini oching, tokenni yozing, saqlang va yopib qayta ishga tushiring.
notepad .env
pause
exit /b
:run
python bot.py
pause
