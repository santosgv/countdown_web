from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Core'

    def ready(self):
        from django.db.models.signals import pre_save
        from .models import UserProfile
        from .signals import create_user_profile