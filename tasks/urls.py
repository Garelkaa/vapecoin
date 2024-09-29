from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TasksView.as_view(), name='main'),
    path('tasks/start/<int:task_id>/', views.StartTaskView.as_view(), name='start_task'),
    path('tasks/get/<int:task_id>/', views.GetTaskView.as_view(), name='get_task'),
]
