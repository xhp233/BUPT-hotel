@echo off
if not exist BUPTHotelAC.db (
    python manage.py makemigrations
    python manage.py migrate
)
python manage.py runserver