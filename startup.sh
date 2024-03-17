#!/bin/bash
python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --workers 2 --bind 0.0.0.0:8000 ninthdjango.wsgi