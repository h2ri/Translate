#!/bin/sh

sleep 5

cd translation_caching
su -m myuser -c "python manage.py makemigrations translation_caching"
su -m myuser -c "python manage.py migrate"
su -m myuser -c "python manage.py runserver 0.0.0.0:8000"
