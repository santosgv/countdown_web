from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from . models import UserProfile,Arquivos
from django.contrib import auth
from django.contrib import messages
from django.contrib.messages import constants
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from decouple import config
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import CustomUserCreationForm,CustomAuthenticationForm
from .utils import email_html,generate_random_password
from django.utils.decorators import method_decorator
from django.http import JsonResponse,HttpResponse
import os
from django.views import View
from django_multiple_chunk_upload.mixins import UploadMixin,CompleteUploadMixin
stripe.api_key= settings.STRIPE_SECRET_KEY


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            path_template = os.path.join(settings.BASE_DIR, 'Core/templates/emails/cadastro_confirmado.html')
            base_url = request.build_absolute_uri('/')
            #email_html(path_template, 'Cadastro confirmado', [user.email,], username=user.username, base_url=base_url)
            login(request, user)  
            return redirect('/perfil') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    mensagem = request.GET.get('mensagem', None)

    if mensagem:
        messages.success(request, mensagem)
        
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

def add_file(request):
    return render(request,'nova.html')

@login_required(login_url='/login/')  
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

@cache_page(60 * 100)
def ads(request):
    if not settings.DEBUG:
        path = os.path.join(settings.STATIC_ROOT,'ads.txt')
        with open(path,'r') as arq:
            return HttpResponse(arq, content_type='text/plain')
    else:
        path = os.path.join(settings.BASE_DIR,'templates/static/ads.txt')
        with open(path,'r') as arq:
            return HttpResponse(arq, content_type='text/plain')
            
@cache_page(60 * 100)
def robots(request):
    if not settings.DEBUG:
        path = os.path.join(settings.STATIC_ROOT,'robots.txt')
        with open(path,'r') as arq:
            return HttpResponse(arq, content_type='text/plain')
    else:
        path = os.path.join(settings.BASE_DIR,'templates/static/robots.txt')
        with open(path,'r') as arq:
            return HttpResponse(arq, content_type='text/plain')

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return UserProfile.objects.all()

    def lastmod(self, obj):
        return obj.data
    
def erro(request):
    return HttpResponse('<h1>Ocorreu um erro ao processar o pagamento</h1><p>Tente novamente ou mais tarde.</p> <a href="/">voltar</a>')

class CreateStripeCheckoutSessionView(View):
    
    def post(self, request, *args, **kwargs):
        base_url = request.build_absolute_uri('/')
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card",'boleto'],
            line_items=[
                {
                    "price_data": {
                        "currency": "brl",
                        "unit_amount": int(9) * 100,
                        "product_data": {
                            "name": 'Contador de Eventos',
                            "description": '1 ano de acesso',
                        },
                    },
                    "quantity": 1,
                }
            ],
            metadata={"product_id": 1},
            mode="payment",
            success_url= base_url + 'login?mensagem=Seu+login+foi+criado+com+sucesso!+Verifique+o+e-mail+cadastrado+no+pagamento+para+mais+detalhes.',
            cancel_url= base_url + 'erro',
        )
        return redirect(checkout_session.url)

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
        
        customer_email = session['customer_details']['email']
        customer_name = session['customer_details']['name']
        
        path_template = os.path.join(settings.BASE_DIR, 'Core/templates/emails/email.html')

        if not User.objects.filter(email=customer_email).exists():
            random_password = generate_random_password(8)
            user = User.objects.create_user(username=customer_email, first_name=customer_name, email=customer_email, password=random_password)
            user.save()
            
            email_html(path_template, 'Usuário Criado com Sucesso', [customer_email, 'santosgomesv@gmail.com'], customer_name=customer_name, usuario=user, password=random_password)
        else:
            email_html(path_template, 'Pagamento realizado', [customer_email, 'santosgomesv@gmail.com'], customer_name=customer_name)

    return HttpResponse(status=200)

@method_decorator([csrf_exempt],name="dispatch")
class UploadView(View,UploadMixin):
    MODEL_CLASS = Arquivos
    FILE_FIELDS = ['file']
    UPLOAD_TO='foto_img'

    def post(self, request):
        file = request.FILES.get('file')
        if file.size > settings.MAX_BYTES:
            return JsonResponse({"error": "O arquivo deve ter no máximo 150 MB."}, status=400)

        return self.handle_chunk_upload(
            request, self.FILE_FIELDS, self.MODEL_CLASS, self.UPLOAD_TO
        )

@method_decorator([csrf_exempt],name="dispatch")
class CompleteUpload(View,CompleteUploadMixin):
    MODEL_CLASS = Arquivos
    NON_FILE_FIELDS =['nome']

    def post(self,request):
        nome = request.POST.get('nome')
        return self.handle_complete_upload(
            request, self.NON_FILE_FIELDS, self.MODEL_CLASS
        )

        if response.status_code == 200:
            arquivo = self.MODEL_CLASS.objects.get(id=response.data['id'])  # Obtém o objeto criado
            arquivo.nome = nome  # Atribui o nome ao arquivo
            arquivo.save()  # Salva o objeto atualizado
        return response