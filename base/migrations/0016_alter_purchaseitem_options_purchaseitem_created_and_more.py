# Generated by Django 4.0.3 on 2022-04-24 16:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_alter_profile_lastmessagesent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchaseitem',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
