import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator
from django.core.asgi import get_asgi_application
import session_emulator.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tender_hack_back.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": OriginValidator(AuthMiddlewareStack(
        URLRouter(
            session_emulator.routing.websocket_urlpatterns
        )
    ),
        ["*"]
    ),
})
