from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto =  models.ImageField(upload_to='foto_img',blank=True, null=True)
    titulo = models.CharField(max_length=250,default="Meu Compromisso")
    data = models.DateTimeField()
    font_color = models.CharField(max_length=7, default='#000000')  
    background_color = models.CharField(max_length=7, default='#FFFFFF')  

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