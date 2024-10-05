from typing import Any
from django.shortcuts import render
from django.views.generic.base import TemplateView

from users.models import Users


class WalletView(TemplateView):
    template_name = 'wallet.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        user = Users.objects.get(pk=self.request.user.id)
        context['user'] = user
        return context
        
