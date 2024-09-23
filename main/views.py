import json
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import View
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from users.models import DailyReward, UserRewardProgress, Users

class MainView(TemplateView):
    template_name = 'index.html'
    
    # Переопределяем метод для передачи дополнительных данных в шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile, created = Users.objects.get_or_create(pk=1)
        rewards = DailyReward.objects.all()
        user_progress, create = UserRewardProgress.objects.get_or_create(user=user_profile)
        
        # Обновляем данные о наградах для пользователя
        for reward in rewards:
            reward.checked = reward.day <= user_progress.consecutive_days  # Проверяем, получена ли награда
        context['rewards'] = rewards
        
        context['user_profile'] = user_profile
        return context
    

@method_decorator(csrf_exempt, name='dispatch')
class UpdateUserDataView(View):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            balance = int(data.get('balance'))
            user_profile, created = Users.objects.get_or_create(pk=1)
            user_profile.money += balance
            user_profile.save()

            return JsonResponse({'success': True})

        except (json.JSONDecodeError, TypeError, ValueError) as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        
        
@method_decorator(csrf_exempt, name='dispatch')
class UpdateDataPresentView(View):

    def post(self, request, *args, **kwargs):
        user, created = Users.objects.get_or_create(pk=1)

        user_reward, created = UserRewardProgress.objects.get_or_create(user=user)

        today = timezone.now().date()

        # Проверяем, если сегодня награда еще не была получена
        if user_reward.last_reward_date != today:
            # Увеличиваем серию и обновляем дату получения награды
            user_reward.consecutive_days = (user_reward.consecutive_days % 7) + 1
            user_reward.last_reward_date = today

            # Рассчитываем награду на основе текущего дня
            next_day = user_reward.consecutive_days
            reward = DailyReward.objects.get(day=next_day)

            # Логика выдачи награды пользователю
            user.money += reward.value
            user.save()
            user_reward.save()

        return redirect('main:main')
    
    
class LiquidView(TemplateView):
    template_name = 'liquid.html'
    
    
class AccumulatorView(TemplateView):
    template_name = 'accumulator.html'
    