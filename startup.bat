@echo off
cd /d %~dp0

call venv\Scripts\activate

cd PartyPictures

python manage.py runserver 0.0.0.0:8000

pause