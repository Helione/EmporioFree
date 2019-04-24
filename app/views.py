from django.shortcuts import render,get_object_or_404, redirect
from django.contrib. auth.decorators import login_required
from .models import Produto, Compra
from django.contrib import messages
# Create your views here.

def lista_produtos(request):
    produtos=Produto.objects.all()
    return render(request,'listaprodutos.html', {'produtos':produtos})

def detalhes(request, slug):
    produto=get_object_or_404(Produto, slug=slug)
    context = {
        'produto':produto
    }
    template_name= 'detalheprodutos.html'
    return render(request, template_name,context)

@login_required
def compra(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    compra, created = Compra.objects.get_or_create(
        user =request.user, produto=produto
    )
    if created:
    #    compra.active()  valor default = 0

        messages.success(request, 'Compra realizada com sucesso!')
    else:
        messages.success(request, 'A compra já foi realizada!')

    return redirect('comprando')

@login_required
def cancelar_compra(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    compra = get_object_or_404(                           #Se existir compra
        Compra, user=request.user, produto=produto
    )
    if request.method == 'POST':   #página de confirmaçao
        compra.delete()
        messages.success(request, 'Sua compra foi cancelada com sucesso')
        return redirect('painel')
    context = {
        'compra': compra,
        'produto': produto,
    }
    return render(request, 'cancelar_compra.html', context)

@login_required
def anuncios(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    if not request.user.is_staff:
        compra= get_object_or_404(
            Compra,user=request.user, produto=produto
        )
        if not compra.is_approved():
            messages.error(request, 'A sua compra está pendente')
            return redirect('painel')
    context = {
        'produto': produto
    }
    return render(request,'anuncios.html', context)