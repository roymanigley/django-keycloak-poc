#!/bin/sh

python ./manage.py collectstatic --noinput
python ./manage.py migrate
python ./manage.py compilemessages

gunicorn config.wsgi:application --workers=3 --bind 0.0.0.0:80