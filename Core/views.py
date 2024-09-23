from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from . models import UserProfile
from django.contrib import auth
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from decouple import config
import requests
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
import json
from django.http import JsonResponse
from django.core.mail import send_mail


stripe.api_key= settings.STRIPE_SECRET_KEY

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
        form = UserProfileForm(request.POST,request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('/perfil')
        return redirect('/login')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'profile.html', {'form': form})


def shared(request,user_id):
    usuario = get_object_or_404(UserProfile, user=user_id)
    return render(request, 'shared.html',{'user':usuario})

def home(request):
    return render(request,'home.html')


def checkout(request):
    return render(request,'checkout.html',{'STRIPE_PUBLIC_KEY': settings.STRIPE_PUPLIC_KEY})

def erro(request):
    return HttpResponse('Erro')

def create_checkout_session(request, id):
    YOUR_DOMAIN = "http://127.0.0.1:8000"
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                'currency': 'BRL',
                'unit_amount': int(29 * 100),
                    'product_data': {
                        'name': 'Contador'
                    }

                },
                'quantity': 1,
            },
        ],
        payment_method_types=[
            'card',
            'boleto',
        ],
        metadata={
            'id_produto': 1,
        },
        mode='payment',
        success_url=YOUR_DOMAIN + '/register',
        cancel_url=YOUR_DOMAIN + '/erro',
    )
    return JsonResponse({'id': checkout_session.id})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        mensagem =f'''
        Pagamento realizado

        '''
        return send_mail('Pagamento realizado com sucesso',mensagem,'santosgomesv@gmail.com',recipient_list=[session['metadata']['email'],])
        

    return HttpResponse(status=200)