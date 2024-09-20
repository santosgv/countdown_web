from django.urls import path
from Core import views

app_name = 'Core'

urlpatterns = [
    path('', views.home, name='home'),
    path('perfil/',views.profile,name='perfil'),
    path('shared/<int:user_id>/',views.shared , name='shared'),
]