# Generated by Django 4.1.3 on 2022-11-26 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GAMES', '0002_alter_game_status_alter_match_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.IntegerField(choices=[(0, 'off'), (1, 'on')], default=0),
        ),
        migrations.AlterField(
            model_name='match',
            name='status',
            field=models.IntegerField(choices=[(0, 'waiting'), (1, 'running'), (2, 'end')], default=0),
        ),
    ]
