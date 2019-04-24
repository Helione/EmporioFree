from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset
from app.models import Compra

from app.utils import generate_hash_key

User = get_user_model()

@login_required
def carrinho(request):
    context ={}
    context['compras'] = Compra.objects.filter(user=request.user)
    return render(request,'carrinho.html', context)

@login_required
def painel(request):
    context = {}
    return render(request,'painel.html', context)

@login_required
def comprando(request):
    context = {}
    return render(request,'comprando.html', context)

def register(request):
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():  # se o formulário for válido
           user = form.save()  # cria um novo usuario a partir dos dados enviados
           user = authenticate(
               username = user.username, password = form.cleaned_data['password1']
           )
           login(request,user)
           return redirect('home')  # redireciona para a tela de login
    else:
            # mostra novamente o formulario de cadastro com os erros do formulario atual
        form = RegisterForm()
    context = {
            'form': form
        }
    return render(request, "register.html", context)
        # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulário

def recuperar_senha(request):

    context = {}
    form = PasswordResetForm(request.POST or None)

    if form.is_valid():
        user = User.objects.get(form.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        context['sucess'] = True
    context['form'] = form
    return render(request, 'recuperar_senha.html', context)

@login_required
def editar(request):
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Os dados da sua conta foram alterados com sucesso!')
            return redirect('painel')
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request,'editar.html', context)

@login_required
def editar_senha(request):
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['sucess'] = True
        return redirect('painel')
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, 'editar_senha.html', context)

