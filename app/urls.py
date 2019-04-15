from django.contrib import admin
from django.urls import path, include
from .views import lista_produtos, detalhes, compra,anuncios,cancelar_compra

urlpatterns = [
       path('', lista_produtos, name='listaprodutos'),
       path('<slug:slug>/', detalhes, name='detalhes'),
       path('<slug:slug>/comprar/', compra, name='comprar'),
       path('<slug:slug>/anuncios/', anuncios, name='anuncios'),
       path('<slug:slug>/cancelar_compra/', cancelar_compra, name='cancelar_compra'),
]
