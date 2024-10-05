from django.urls import path
from django.conf.urls.static import static
from vapecoin import settings
from . import views

app_name = 'shop'

urlpatterns = [
    path("", views.ShopView.as_view(), name='main')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
