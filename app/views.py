from django.shortcuts import render,get_object_or_404, redirect
from django.contrib. auth.decorators import login_required
from .models import Produto, Compra,Comentario, Caracteristicas, Categoria
from django.contrib import messages

from .forms import ComentarioForm
from .decorators import compra_required
# Create your views here.

def lista_produtos(request):
    categorias = Categoria.objects.all()
    produtos=Produto.objects.all()

    var_get_search = request.GET.get('search_box')
    if var_get_search is not None:
        produtos = produtos.filter(nome__icontains=var_get_search)
    context = {
        'produtos' : produtos,
        'categorias':categorias,
    }
    return render(request,'listaprodutos.html', context)

def categoria(request,slug):
    categorias = Categoria.objects.all()
    categoria = get_object_or_404(Categoria, slug=slug)

    context = {
        'produtos': Produto.objects.filter(categoria=categoria),
        'categoria': categoria,
        'categorias':categorias,
    }
    return render(request,'categorias.html',context)

def trabalhe_conosco(request):
    return render(request,'trabalhe_conosco.html')

def detalhes(request, slug):
    categorias = Categoria.objects.all()
    produto=get_object_or_404(Produto, slug=slug)
    caracteristicas = get_object_or_404(produto.caracteristicas.all())


    context = {
        'produto':produto,
        'detalhes':produto.detalhes.all(),
        'caracteristicas': caracteristicas,
        'categorias':categorias,
    }
    template_name= 'detalheprodutos.html'
    return render(request, template_name,context)

def pesquisar_nomes(request):
    produtos=Produto.objects.all()
    search_fields = ['produto', 'inftecnica']
    var_get_search = request.GET.get('search_fields')
    if var_get_search is not None:
        produtos = produtos.filter(nome__icontains=var_get_search)

    context = {
        'search_fields':search_fields,
        'produtos':produtos
    }
    return render(request,'base.html',context)


def caracteristicas(request, slug, id):

    produto = get_object_or_404(Produto, slug=slug)
    caracteristicas = get_object_or_404(produto.caracteristicas.all(), pk=id)
    categorias = Categoria.objects.all()

    context = {
        'produto': produto,
        'caracteristicas': caracteristicas,
        'categorias':categorias,
    }
    return render(request, 'informacoes_produtos.html', context)

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

    return redirect('painel')

@login_required
def cancelar_compra(request, slug):
    categorias = Categoria.objects.all()
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
        'categorias':categorias,
    }
    return render(request, 'cancelar_compra.html', context)

@login_required
@compra_required
def anuncios(request, slug):
    categorias = Categoria.objects.all()
    produto = request.produto
    context = {
        'produto': produto,
        'categorias':categorias
    }
    return render(request,'anuncios.html', context)

@login_required
def show_comentario(request, slug, id):
    categorias = Categoria.objects.all()
    produto = get_object_or_404(Produto, slug=slug)
    caracteristicas = get_object_or_404(produto.caracteristicas.all())
    detalhe = get_object_or_404(produto.detalhes.all(), pk=id)

    form = ComentarioForm(request.POST or None)
    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.user = request.user
        comentario.detalhe = detalhe
        comentario.save()
        form = ComentarioForm()
        messages.success(request, 'Seu comentário foi enviado com sucesso! ')

    template = 'show_comentario.html'
    context = {
        'produto': produto,
        'detalhe': detalhe,
        'caracteristicas':caracteristicas,
        'form': form,
        'categorias':categorias,
    }
    return render(request, template, context)

@login_required
@compra_required
def sobre_produto(request, slug):
    categorias = Categoria.objects.all()
    produto=get_object_or_404(Produto, slug=slug,)
    caracteristicas = get_object_or_404(produto.caracteristicas.all())

    context = {
        'produto': produto,
        'categorias':categorias,
        'cacteristicas':caracteristicas,
    }
    return render(request,'sobre_produto.html', context)


@login_required
@compra_required
def garantia_produto(request, slug):
    produto=get_object_or_404(Produto, slug=slug,)
    categorias = Categoria.objects.all()
    context = {
        'produto': produto,
        'categorias': categorias,
    }
    return render(request,'garantia_produto.html', context)

@login_required
@compra_required
def fornecedores_produto(request, slug):
    produto=get_object_or_404(Produto, slug=slug,)
    categorias = Categoria.objects.all()

    context = {
        'produto': produto,
        'categorias': categorias,
    }
    return render(request,'fornecedores_produto.html', context)

@login_required
@compra_required
def forum_de_duvidas(request,slug):
    produto=get_object_or_404(Produto, slug=slug,)
    categorias = Categoria.objects.all()
    context = {
        'produto': produto,
        'categorias': categorias,
    }
    return render(request,'forum_de_duvidas.html',context)