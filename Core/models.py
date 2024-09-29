from django.db import models
from django.contrib.auth.models import User
import os
from django.utils import timezone
from django_multiple_chunk_upload.models import ChunkUpload


class Arquivos(ChunkUpload):
    nome = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to='foto_img',blank=True, null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto =  models.OneToOneField(Arquivos,on_delete=models.CASCADE,null=True, blank=True)
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

