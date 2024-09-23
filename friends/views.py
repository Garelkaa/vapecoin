from typing import Any
from django.shortcuts import render
from django.views.generic.base import TemplateView


class FriendsView(TemplateView):
    template_name = 'friends.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(**kwargs)
        
