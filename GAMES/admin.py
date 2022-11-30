from django.contrib import admin

from GAMES.models import *
from Accounts.forms import CustomUserCreationForm
from .forms import *


# Register your models here.


class CustomGAMEAdmin(admin.ModelAdmin):
    model = Game
    list_display = ['id', 'name', 'author', 'rule', 'status']
    search_fields= ['id', 'name', 'author__username','status']

admin.site.register( Game,CustomGAMEAdmin )


class CustomMatchAdmin(admin.ModelAdmin):
    model = Match
    search_fields = ['id', 'game__name', 'id_play1', 'id_play2']
    list_display = ['id', 'game', 'id_play1', 'id_play2', 'score_play1', 'score_play2', 'status']


admin.site.register(Match,CustomMatchAdmin)


admin.site.register(Notification)
admin.site.register(Scores)
