from django.template.defaulttags import url
from django.urls import path

from GAMES.views import home,games,match_home,scores,delete_noti,delete_game,match

app_name = "game"
urlpatterns = [
    path('', games, name='game'),
    path('matchs/', match_home, name='match_home'),
    path('scores/', scores, name='scores'),
    path('delete_noti/<id>',delete_noti,name='delete_noti'),
    path('delete_game/<id>',delete_game,name='delete_game'),
    path('matchs/<str:id>/', match, name='match'),
]