# Generated by Django 4.0.3 on 2022-04-02 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_purchaseitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchaseitem',
            options={'ordering': ['-item']},
        ),
        migrations.RenameField(
            model_name='purchaseitem',
            old_name='name',
            new_name='item',
        ),
    ]
