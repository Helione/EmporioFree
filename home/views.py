#https://docs.djangoproject.com/en/2.1/topics/auth/default/#built-in-auth-forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from app.models import Categoria,Produto


def home(request):
    categorias = Categoria.objects.all()
    produtos=Produto.objects.all()

    var_get_search = request.GET.get('search_box')
    if var_get_search is not None:
       produtos = produtos.filter(nome__icontains=var_get_search)

    context = {
        'categorias': categorias,
        'produtos':produtos,
    }

    return render(request,'home.html',context)

def my_logout(request):
    logout(request)
    return redirect('home')


#https://www.devmedia.com.br/como-criar-um-blog-com-django-e-python/33710