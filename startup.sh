#!/bin/bash
python python manage.py collectstatic && gunicorn --workers 2 ninthdjango.wsgi