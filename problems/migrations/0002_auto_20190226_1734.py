# Generated by Django 2.1.1 on 2019-02-26 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='problems',
            field=models.ManyToManyField(blank=True, to='problems.Problem'),
        ),
    ]
