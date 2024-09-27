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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile, created = Users.objects.get_or_create(pk=1)
        rewards = DailyReward.objects.all()
        user_progress, create = UserRewardProgress.objects.get_or_create(user=user_profile)
        
        for reward in rewards:
            reward.checked = reward.day <= user_progress.consecutive_days
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
        
        if user_reward.last_reward_date != today:
            user_reward.consecutive_days = (user_reward.consecutive_days % 7) + 1
            user_reward.last_reward_date = today

            next_day = user_reward.consecutive_days
            reward = DailyReward.objects.get(day=next_day)

            user.money += reward.value
            user.save()
            user_reward.save()

        return redirect('main:main')
    
    
class LiquidView(TemplateView):
    template_name = 'liquid.html'
    
    
class AccumulatorView(TemplateView):
    template_name = 'accumulator.html'
    