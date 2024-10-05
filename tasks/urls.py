from django.urls import path
from django.conf.urls.static import static
from vapecoin import settings
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TasksView.as_view(), name='main'),
    path('tasks/start/<int:task_id>/', views.StartTaskView.as_view(), name='start_task'),
    path('tasks/get/<int:task_id>/', views.GetTaskView.as_view(), name='get_task'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
