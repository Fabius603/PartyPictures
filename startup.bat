@echo off
REM — Projekt-Root als Arbeitsverzeichnis setzen
cd /d %~dp0

REM — Virtuelle Umgebung aktivieren
call venv\Scripts\activate

cd PartyPictures

REM — Django-Entwicklungsserver starten (im LAN erreichbar)
python manage.py runserver 0.0.0.0:8000

REM — Fenster offen halten, bis eine Taste gedrückt wird
pause