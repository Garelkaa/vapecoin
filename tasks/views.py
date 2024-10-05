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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(Users, pk=self.request.user.id)  # Fetch the current user
        tg_tasks = Tasks.objects.filter(category='TG')
        youtube_tasks = Tasks.objects.filter(category='YouTube')

        # Retrieve the status of each YouTube task for the current user
        youtube_tasks_with_status = []
        for task in youtube_tasks:
            try:
                task_user = TasksUser.objects.get(user=user, task=task)
                youtube_tasks_with_status.append((task, task_user.status))
            except TasksUser.DoesNotExist:
                # If there's no entry in TasksUser for the user-task combination, treat it as not started
                youtube_tasks_with_status.append((task, None))
        
        tg_tasks_with_status = []
        for task in tg_tasks:
            try:
                task_user = TasksUser.objects.get(user=user, task=task)
                tg_tasks_with_status.append((task, task_user.status))
            except TasksUser.DoesNotExist:
                # If there's no entry in TasksUser for the user-task combination, treat it as not started
                tg_tasks_with_status.append((task, None))

        context['user'] = user
        context['tg_tasks'] = tg_tasks
        context['youtube_tasks'] = youtube_tasks_with_status
        context['tg_tasks'] = tg_tasks_with_status# Use the list of tasks with their statuses
        return context


class StartTaskView(View):
    def get(self, request, task_id):
        user = Users.objects.get(pk=request.user.id)  # Replace this with the actual user logic
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
        user = Users.objects.get(pk=request.user.id)  # Замените это на логику получения пользователя
        task = get_object_or_404(Tasks, pk=task_id)


        reward = int(task.reward)

        task_user = get_object_or_404(TasksUser, user=user, task=task, status='checked')
        task_user.status = 'done'
        task_user.save()

        user.money += reward
        user.save()

        # Перенаправляем обратно на страницу задач
        return redirect(reverse('tasks:main'))
    
