from django.urls import re_path
from . import consumers

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/channels/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # re_path(r'ws/channels/(?P<room_name>\w+)/$', consumers.Games.as_asgi()),
]