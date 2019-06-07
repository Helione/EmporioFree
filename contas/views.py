from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate,login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset
from app.models import Compra,Produto,Categoria

from app.utils import generate_hash_key

User = get_user_model()

@login_required
def carrinho(request):
    context ={}
    context['compras'] = Compra.objects.filter(user=request.user)
    return render(request,'carrinho.html', context)

@login_required
def painel(request):
    categorias = Categoria.objects.all()
    produtos=Produto.objects.all()

    var_get_search = request.GET.get('search_box')
    if var_get_search is not None:
        produtos = produtos.filter(nome__icontains=var_get_search)
    context = {
        'produtos' : produtos,
        'categorias':categorias,
    }
    return render(request,'painel.html', context)

@login_required
def comprando(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    context = {
        'produto' : produto
    }
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
        context['success'] = True
    context['form'] = form
    return render(request, 'recuperar_senha.html', context)

@login_required
def editar(request):
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Os Dados foram alterados com Sucesso!')
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
            context['success'] = True
        return redirect('painel')
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, 'editar_senha.html', context)



#http://pythonclub.com.br/tutorial-django-17.html
#https://simpleisbetterthancomplex.com/tips/2016/09/06/django-tip-14-messages-framework.html