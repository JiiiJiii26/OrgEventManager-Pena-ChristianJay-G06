"""
ASGI config for OrgEventManager project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orgevent.settings')

application = get_asgi_application()
