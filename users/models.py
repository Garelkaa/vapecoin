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
    energy = models.IntegerField(null=True, blank=True, default=1000)
    objects = CustomUserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'user_id_tg'
    class Meta:
        db_table = "users"
        
        
class Refferer(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, related_name='users_id')
    ref_link = models.TextField(null=True, blank=True)
    ref_user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, related_name='user_id_referal')
        