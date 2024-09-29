from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, user_id_tg, **extra_fields):
        """
        Creates and saves a User with the given user_id_tg.
        """
        if not user_id_tg:
            raise ValueError('The user_id_tg must be set')
        
        user = self.model(user_id_tg=user_id_tg, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id_tg, **extra_fields):
        """
        Creates and saves a superuser with the given user_id_tg.
        """
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(user_id_tg, **extra_fields)


class Users(AbstractBaseUser):
    user_id_tg = models.BigIntegerField(unique=True, null=True, blank=True)  # Add unique=True here
    money = models.IntegerField(null=True, blank=True)
    moneyhour = models.IntegerField(null=True, blank=True)
    energy = models.IntegerField(null=True, blank=True, default=1000)
    username_tg = models.TextField(null=True, blank=True)
    username_custom = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    stop_refill = models.BooleanField(default=False)
    last_visit = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def update_money_on_visit(self):
        now = timezone.now()  # Текущее время
        
        # Если last_visit не задано (например, первый визит)
        if self.last_visit is None:
            self.last_visit = now
            self.save()  # Сохраняем первое посещение и выходим
            return

        # Вычисляем разницу во времени
        time_delta = now - self.last_visit
        hours_passed = int(time_delta.total_seconds() // 3600)  # Количество полных часов

        # Если прошло больше или равно 1 часу
        if hours_passed >= 1:
            # Начисляем деньги
            self.money += hours_passed * self.moneyhour
            
            # Обновляем время последнего визита
            self.last_visit = now
            self.save()
    objects = CustomUserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'user_id_tg'
    class Meta:
        db_table = "users"
        
        
        
class Refferer(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, related_name='users_id')
    ref_link = models.TextField(null=True, blank=True)
    ref_user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, related_name='user_id_referal')
        
        
class DailyReward(models.Model):
    day = models.IntegerField(null=True, blank=True)  # День (например, День 1, День 2 и т.д.)
    reward = models.CharField(max_length=255, null=True, blank=True)  # Награда (например, монеты, предметы)
    value = models.IntegerField(null=True, blank=True)  # Количество награды

    def __str__(self):
        return f'Награда за день {self.day}: {self.reward} ({self.value})'


class UserRewardProgress(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, null=True, blank=True)  # Пользователь
    last_reward_date = models.DateField(null=True, blank=True)  # Дата последней награды
    consecutive_days = models.IntegerField(null=True, blank=True,default=0)  # Количество подряд идущих дней с наградой

    def __str__(self):
        return f'Прогресс пользователя {self.user.username}'
