# Generated by Django 4.0.3 on 2022-04-01 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pointsReceived',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='pointsToSend',
            field=models.IntegerField(default=100),
        ),
    ]
