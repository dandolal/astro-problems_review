# Generated by Django 2.1.1 on 2019-04-23 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0007_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='player_id',
            field=models.IntegerField(default=-1),
        ),
    ]