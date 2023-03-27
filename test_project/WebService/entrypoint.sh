#!/bin/sh
python3 manage.py makemigrations &
python3 manage.py migrate &
python3 manage.py collectstatic --no-input &
gunicorn -b 0.0.0.0:8000 ws_test.wsgi:application & 
daphne -b 0.0.0.0 -p 9000 ws_test.asgi:application;
