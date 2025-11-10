@echo off
cd /d C:\Users\vitor\Documents\lembretes_project
call .venv\Scripts\activate.bat
if not exist logs mkdir logs
python manage.py send_reminders >> logs\reminders.log 2>&1
deactivate
