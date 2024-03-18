"""
ASGI config for ninthdjango project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from .models import Videos
from django.contrib import admin

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ninthdjango.settings')

application = get_asgi_application()

admin.site.register(Videos)