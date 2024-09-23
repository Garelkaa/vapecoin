from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('update-data/', views.UpdateUserDataView.as_view(), name='update_data'),
    path('daily-reward/', views.UpdateDataPresentView.as_view(), name='daily_reward'),
    path('liquid/', views.LiquidView.as_view(), name='liquid'),
    path('accumulator/', views.AccumulatorView.as_view(), name='accumulator'),
]
