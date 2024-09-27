from typing import Any
from django.shortcuts import render
from django.views.generic.base import TemplateView

from users.models import Refferer


class FriendsView(TemplateView):
    template_name = 'friends.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        refferals = Refferer.objects.filter(ref_user_id_id=1)
        refferals_count = Refferer.objects.filter(ref_user_id_id=1).count()
        reff_link = Refferer.objects.filter(user_id=1).first().ref_link
        context['refferals'] = refferals
        context['reff_link'] = reff_link
        context['refferals_count'] = refferals_count
        return context
