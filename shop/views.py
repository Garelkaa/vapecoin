from django.views.generic.base import TemplateView

class ShopView(TemplateView):
    template_name = 'market.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context