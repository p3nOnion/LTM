from django import forms
from django_registration.forms import RegistrationForm
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from numpy import require

from GAMES.models import *
from Accounts.models import Users


class CustomUserCreationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = Users
        fields = ('username', 'email', 'score')


class NewGameForm(forms.Form):
    error_messages = {
        "name_valid": (f'The name "%s" is not valid'),
        "id1_valid": (f'The id1 "%s" is not valid'),
        "id2_valid": (f'The id2 "%s" is not valid'),
    }
    name = forms.CharField(max_length=100)
    ip = forms.CharField(max_length=200)
    port = forms.IntegerField()
    rule = forms.FileField()

    def clean_rule(self):
        rule = self.cleaned_data.get("rule")
        return rule

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Game.objects.filter(name=name).first() is not None:
            raise ValidationError(
                self.error_messages["email_valid"] % name,
                code="name_valid",
            )
        return name

    class Meta:
        model = Game


class MatchForm(forms.Form):
    error_messages = {
        "name_valid": (f'The name "%s" is not valid'),
        "id1_valid": (f'The id1 "%s" is not valid'),
        "id2_valid": (f'The id2 "%s" is not valid'),
    }
    game = forms.IntegerField()
    id_play1 = forms.IntegerField(required=True)
    id_play2 = forms.IntegerField(required=True)
    password = forms.CharField(max_length=50, required=True)

    def clean_game(self):
        game = self.cleaned_data.get("game")
        if Game.objects.filter(id=game).first() == None:
            raise ValidationError(
                self.error_messages["name_valid"] % game,
                code="game_valid",
            )
        return game

    def clean_id_play1(self):
        id = self.cleaned_data.get("id_play1")
        if id and Users.objects.filter(id=id).first() == None:
            raise ValidationError(
                self.error_messages["id1_valid"] % id,
                code="id1_valid",
            )
        return id
    def clean_id_play2(self):
        id = self.cleaned_data.get("id_play1")
        id2 = self.cleaned_data.get("id_play2")
        if id and id2 and id == id2:
            raise ValidationError(
                self.error_messages["id2_valid"],
                code="id1_valid",
            )
        if Users.objects.filter(id=id2).first() == None:
            raise ValidationError(
                self.error_messages["id2_valid"] % id2,
                code="id1_valid",
            )
        return id2
    class Meta:
        model = Match
