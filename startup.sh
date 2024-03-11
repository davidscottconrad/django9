#!/bin/bash
python manage.py migrate && python manage.py collectstatic --noinput && gunicorn ninthdjango.wsgi --bind 0.0.0.0:8000 --workers 2