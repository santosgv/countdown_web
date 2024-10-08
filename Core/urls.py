from django.urls import path
from Core import views
from django.contrib.sitemaps.views import sitemap
from .views import login_view, logout_view,CreateStripeCheckoutSessionView,ads,robots
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('ads.txt',ads),
    path('robots.txt',robots),

    path('checkout/',views.checkout, name='checkout'),
    path('erro/',views.erro, name='erro'),
    path('register/', views.register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('perfil/',views.profile,name='perfil'),
    path('add_file/',views.add_file, name='add_file'),
    path('upload',views.UploadView.as_view(),name='upload'),
    path('complete',views.CompleteUpload.as_view(),name='complete'),
    path('shared/<int:user_id>/',views.shared , name='shared'),
        path(
        "create-checkout-session/<int:pk>/",
        CreateStripeCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    #path('stripe_webhook', views.stripe_webhook, name="stripe_webhook"),


    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="emails/password_reset.html"), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="emails/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="emails/password_reset_confirm_view.html"), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="emails/password_reset_complete.html"), name="password_reset_complete"),
]