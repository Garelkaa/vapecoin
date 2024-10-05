

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/<int:user_id>/', views.login_view, name='login'),
]
