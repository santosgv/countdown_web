from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from . models import UserProfile
from django.contrib import auth

from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('/perfil') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/perfil')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth.logout(request)
    return redirect('/') 

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('/perfil')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'profile.html', {'form': form})


def shared(request,user_id):
    usuario = get_object_or_404(UserProfile, user=user_id)
    return render(request, 'shared.html',{'user':usuario})

def home(request):
    return render(request,'home.html')


def vendas(request):
    return render(request,'vendas.html')