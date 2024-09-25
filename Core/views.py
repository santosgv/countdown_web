from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from . models import UserProfile
from django.contrib import auth
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from decouple import config
from django.contrib.auth import login
from .forms import CustomUserCreationForm,CustomAuthenticationForm
from .utils import email_html
from django.http import JsonResponse,HttpResponse
import os


stripe.api_key= settings.STRIPE_SECRET_KEY


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            path_template = os.path.join(settings.BASE_DIR, 'Core/templates/emails/cadastro_confirmado.html')
            base_url = request.build_absolute_uri('/')
            email_html(path_template, 'Cadastro confirmado', [user.email,], username=user.username, base_url=base_url)
            login(request, user)  
            return redirect('/perfil') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/perfil')
    else:
        form = CustomAuthenticationForm()
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
        
        amount_total = session['amount_total'] / 100
        customer_email = session['customer_details']['email']
        customer_name = session['customer_details']['name']
        print(f"Pagamento confirmado! Nome: {customer_name}, Email: {customer_email}, Valor: R${amount_total}")
        #return send_mail('Pagamento realizado com sucesso',mensagem,'santosgomesv@gmail.com',recipient_list=[session['metadata']['email'],])
        return email_html(path_template, 'Cadastro confirmado', [email,], username=username, base_url=base_url ,link_ativacao=link_ativacao)
        return JsonResponse({'status': 'success'})

    return HttpResponse(status=200)