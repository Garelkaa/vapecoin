# Generated by Django 4.1.7 on 2024-09-26 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userrewardprogress_remove_dailyreward_reward_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='users',
            name='username_custom',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='username_tg',
            field=models.TextField(blank=True, null=True),
        ),
    ]
