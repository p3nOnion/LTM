# Generated by Django 4.1.3 on 2022-11-27 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GAMES', '0008_scores_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
