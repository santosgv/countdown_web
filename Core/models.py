from django.db import models
from django.contrib.auth.models import User
import os
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto =  models.ImageField(upload_to='foto_img',blank=True, null=True)
    titulo = models.CharField(max_length=250,default="Meu Compromisso")
    data = models.DateTimeField()
    font_color = models.CharField(max_length=7, default='#000000')  
    background_color = models.CharField(max_length=7, default='#FFFFFF')
    valid_until = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return self.user.username

    @property
    def is_video(self):
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv','.webm']
        ext = os.path.splitext(self.UserProfile.foto)[1].lower()
        return ext in video_extensions

    @property
    def is_img(self):
        img_extensions = ['.jpg','.gif','.png']
        ext = os.path.splitext(self.UserProfile.foto)[1].lower()
        return ext in img_extensions
    
    @property
    def is_access_valid(self):
        """Verifica se o acesso do usuário ainda é válido"""
        if self.valid_until:
            return timezone.now() <= self.valid_until
        return False