# Generated by Django 4.1.3 on 2022-11-26 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GAMES', '0007_match_date_create_match_date_end_scores'),
    ]

    operations = [
        migrations.AddField(
            model_name='scores',
            name='score',
            field=models.BigIntegerField(default=0),
        ),
    ]
