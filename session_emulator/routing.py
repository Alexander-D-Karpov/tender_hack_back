import os

import django
from django.urls import re_path

from session_emulator import consumers


os.environ["DJANGO_SETTINGS_MODULE"] = "tender_hack_back.settings"
django.setup()


websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
