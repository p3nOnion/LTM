# Generated by Django 3.2.16 on 2022-11-26 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_alter_users_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
