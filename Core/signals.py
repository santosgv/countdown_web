from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from datetime import datetime, timedelta

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            titulo="Meu Compromisso",  # Define um título padrão
            data=datetime.now() + timedelta(days=2),  # Define a data para 2 dias a partir de agora
        )

# Salva o perfil de usuário quando o usuário é salvo
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()