from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['font_color', 'background_color','titulo','data']
        widgets = {
             'data': forms.DateTimeInput(format='%Y-%m-%dT%H:%M:%S',attrs={'type': 'datetime-local'}),
            'font_color': forms.TextInput(attrs={'type': 'color'}),
            'background_color': forms.TextInput(attrs={'type': 'color'}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Obrigatório. Informe um e-mail válido.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user