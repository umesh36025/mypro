import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ems.settings")

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
django_Asgi_app=get_asgi_application()

import ems.routing as routing

application = ProtocolTypeRouter({
    "http": django_Asgi_app,
    "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        ))
    ),
})