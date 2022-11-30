from django.template.defaulttags import url
from django.urls import path

from Channels.views import lobby,room

app_name = "channels"
urlpatterns = [
    path(r'', lobby, name='user_list'),

    path('<str:room_name>/', room, name='room'),
]
