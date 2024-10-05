from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class CustomBackend(BaseBackend):
    def authenticate(self, request, user_id_tg=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(user_id_tg=user_id_tg)
            return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None