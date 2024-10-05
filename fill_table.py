import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vapecoin.settings")

import django
django.setup()

from users.models import Users, DailyReward
from tasks.models import Tasks

def check_empty_table(model):
    return model.objects.exists()

def generate_cinema_data():
    if not check_empty_table(Users):
        
        Users.objects.create(
            user_id_tg='123',
            password='123'
        )
        
        print("+")
        

def generate_tasks_data():
    if not check_empty_table(Tasks):
        for _ in range(1):
            Tasks.objects.create(
                name='Youtube',
                category='YouTube',
                reward=10000,
                url='https://youtube.com'
            )
        for _ in range(1):
            Tasks.objects.create(
                name='Подпишись на канал',
                category='TG',
                reward=10000,
                url='https://t.me/vape_comunnity'
            ) 


def generate_dailyrevard_data():
    if not check_empty_table(DailyReward):
        for _ in range(1):
            DailyReward.objects.create(
                day=1,
                reward='монеты',
                value=10000,
            )
        for _ in range(1):
            DailyReward.objects.create(
                day=2,
                reward='монеты',
                value=10000,
            )
        for _ in range(1):
            DailyReward.objects.create(
                day=3,
                reward='монеты',
                value=10000,
            )
        for _ in range(1):
            DailyReward.objects.create(
                day=4,
                reward='монеты',
                value=10000,
            )
        for _ in range(1):
            DailyReward.objects.create(
                day=5,
                reward='монеты',
                value=10000,
            )
        for _ in range(1):
            DailyReward.objects.create(
                day=6,
                reward='монеты',
                value=10000,
            )
        for _ in range(1):
            DailyReward.objects.create(
                day=7,
                reward='монеты',
                value=10000,
            )
        for _ in range(1):
            DailyReward.objects.create(
                day=8,
                reward='монеты',
                value=10000,
            )
        for _ in range(1):
            DailyReward.objects.create(
                day=9,
                reward='монеты',
                value=10000,
            )
        for _ in range(1):
            DailyReward.objects.create(
                day=10,
                reward='монеты',
                value=10000,
            )
# Example list

# Call the functions to generate data
generate_cinema_data()
generate_tasks_data()
generate_dailyrevard_data()