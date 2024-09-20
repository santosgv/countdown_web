from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from . models import UserProfile


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