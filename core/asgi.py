
#core/asgi.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()  # Configura Django antes de importar cosas que usan modelos

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from core.middleware import TokenAuthMiddleware
import apps.produccion.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter(
            apps.produccion.routing.websocket_urlpatterns
        )
    ),
})
