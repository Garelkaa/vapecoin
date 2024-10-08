# Generated by Django 4.1.7 on 2024-09-22 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_users_moneyhour'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.PositiveIntegerField()),
                ('reward_amount', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserDailyReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_claim_date', models.DateField(blank=True, null=True)),
                ('current_streak', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
