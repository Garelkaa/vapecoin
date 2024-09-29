from typing import Any
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView, View
from django.urls import reverse
import requests
from tasks.models import Tasks, TasksUser
from users.models import Users


class TasksView(TemplateView):
    template_name = 'tasks.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = Users.objects.get(pk=1)  # Fetch the current user
        tg_tasks = Tasks.objects.filter(category='TG')
        youtube_tasks = Tasks.objects.filter(category='YouTube')

        context['user'] = user
        context['tg_tasks'] = tg_tasks
        context['youtube_tasks'] = youtube_tasks
        return context


class StartTaskView(View):
    def get(self, request, task_id):
        user = Users.objects.get(pk=1)  # Replace this with the actual user logic
        task = get_object_or_404(Tasks, pk=task_id)

        # Create or update the task status to 'checked'
        task_user, created = TasksUser.objects.get_or_create(
            user=user,
            task=task,
            defaults={'status': 'checked'}
        )

        if not created and task_user.status != 'done':
            task_user.status = 'checked'
            task_user.save()

        # Redirect to the task URL
        return redirect(task.url)


class GetTaskView(View):
    def get(self, request, task_id):
        user = Users.objects.get(pk=1)  # Замените это на логику получения пользователя
        task = get_object_or_404(Tasks, pk=task_id)

        # Проверка подписки только для задачи с task_id == 2
        if task_id == 2:
            check_subscribe_url = 'http://localhost:61616/check_subscribe'
            data = {
                'user_id': user.id,  # или другой идентификатор пользователя
                'channel_id': task.channel_id  # если канал связан с задачей
            }

            response = requests.get(url=check_subscribe_url, json=data)

            # Проверка, подписан ли пользователь
            if response.status_code != 200 or not response.json().get('subscribed', False):
                # Если пользователь не подписан или произошла ошибка
                return HttpResponseForbidden("Вы не подписаны на канал")

        reward = int(task.reward)

        task_user = get_object_or_404(TasksUser, user=user, task=task, status='checked')
        task_user.status = 'done'
        task_user.save()

        user.money += reward
        user.save()

        # Перенаправляем обратно на страницу задач
        return redirect(reverse('tasks:main'))
    