from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    font_color = models.CharField(max_length=7, default='#000000')  # Cor da fonte em formato hexadecimal
    background_color = models.CharField(max_length=7, default='#FFFFFF')  # Cor do fundo em formato hexadecimal

    def __str__(self):
        return self.user.username