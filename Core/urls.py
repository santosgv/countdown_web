from django.urls import path
from Core import views
from .views import login_view, logout_view
from django.contrib.auth import views as auth_views



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


    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="emails/password_reset.html"), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="emails/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="emails/password_reset_confirm_view.html"), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="emails/password_reset_complete.html"), name="password_reset_complete"),
]