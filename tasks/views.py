from typing import Any
from django.shortcuts import render
from django.views.generic.base import TemplateView

from tasks.models import Tasks
from users.models import Users


class TasksView(TemplateView):
    template_name = 'tasks.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        user = Users.objects.get(pk=1)
        tg_tasks = Tasks.objects.filter(category='TG')
        youtube_tasks = Tasks.objects.filter(category='YouTube')
        
        
        context['user'] = user
        context['tg_tasks'] = tg_tasks
        context['youtube_tasks'] = youtube_tasks
        return context
        
