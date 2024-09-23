from django.urls import path
from Core import views
from .views import login_view, logout_view

app_name = 'Core'

urlpatterns = [
    path('', views.home, name='home'),
    path('checkout/',views.checkout, name='checkout'),
    path('erro/',views.erro, name='erro'),
    path('register/', views.register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('perfil/',views.profile,name='perfil'),
    path('shared/<int:user_id>/',views.shared , name='shared'),
   # path('create_checkout_session/<int:id>', views.create_checkout_session, name="create_checkout_session"),
    path('stripe_webhook', views.stripe_webhook, name="stripe_webhook"),
]