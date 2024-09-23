from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
    path('', views.FriendsView.as_view(), name='main')
]
