# Generated by Django 4.0.3 on 2022-04-02 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_message_pointtotal'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cost', models.IntegerField()),
                ('timesPurchased', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-timesPurchased'],
            },
        ),
    ]
