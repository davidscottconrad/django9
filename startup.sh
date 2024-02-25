#!/bin/bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic && gunicorn --workers 2 ninthdjango.wsgi