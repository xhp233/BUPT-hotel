#!/bin/bash
if [ ! -f BUPTHotelAC.db ]; then
    python manage.py makemigrations
    python manage.py migrate
fi
python manage.py runserver