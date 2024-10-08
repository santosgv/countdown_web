from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from datetime import datetime, timedelta
from .utils import email_html
from decouple import config
from django.conf import settings
import os

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            titulo="Meu Compromisso",  
            data=datetime.now() + timedelta(days=2),
            valid_until= datetime.now() + timedelta(days=360)
        )

        print('fui chamado de criar',instance.email,)

# Salva o perfil de usuário quando o usuário é salvo
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    path_template = os.path.join(settings.BASE_DIR, 'Core/templates/emails/cadastro_confirmado.html')
#    instance.userprofile.save()
#    subject = 'Usuario Criado'
#    message = f'''O Usuario {instance.userprofile} foi criado com sucesso
#    valido ate : {instance.userprofile.valid_until}
#    E-mail : {instance.userprofile.user.email}
#    '''
#    from_email = config('EMAIL_HOST_USER')
#    recipient_list = ['santosgomesv@gmail.com',]
#    print('fui chamado salvar')
    #email_html(path_template,subject,{instance.userprofile.user.email})
#    return 'Super Usuario Criado'