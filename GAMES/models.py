from django.db import models
from Accounts.models import Users
from django.utils import timezone
# Create your models here.


class Game(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    ip = models.CharField(max_length=200, default='localhost')
    port = models.IntegerField(default=80)
    rule = models.FileField(upload_to='uploads/')
    is_active = models.BooleanField(default=True)
    STATUS = [
        (0, "off"),
        (1, "on")
    ]
    status = models.IntegerField(choices=STATUS, default=1)

    def __str__(self):
        return self.name+"_"+str(self.id)


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, default=0)
    id_play1 = models.IntegerField(blank=False)
    id_play2 = models.IntegerField(blank=False)
    score_play1 = models.IntegerField(default=0)
    score_play2 = models.IntegerField(default=0)
    date_create = models.DateTimeField(default=timezone.now)
    date_end = models.DateTimeField(default=timezone.now)
    password = models.CharField(max_length=50, blank=False, default='passwd')
    STATUS = [
        (0, "waiting"),
        (1, "running"),
        (2, "end"),
    ]
    history = models.FileField(upload_to='uploads/history/', blank=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return str(self.game)+"_"+str(self.id)


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    ip = models.TextField()
    port = models.IntegerField()
    passwd = models.TextField(default="passwd")

    def __str__(self):
        return str(self.user_id) + "_" + str(self.title)


class Scores(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.user_id) + "_" + str(self.game_id)
