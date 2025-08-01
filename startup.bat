@echo off
cd /d %~dp0

pip install -r .\requirements.txt

cd PartyPictures

python manage.py migrate

python manage.py runserver 0.0.0.0:8077

pause