from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/enviar-foto/', views.enviar_foto, name='enviar_foto'),
    path('api/galeria/', views.galeria_api, name='galeria_api'),
]
