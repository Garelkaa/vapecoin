# Generated by Django 4.1.7 on 2024-09-28 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_users_image_users_username_custom_users_username_tg'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='stop_refill',
            field=models.BooleanField(default=False),
        ),
    ]
