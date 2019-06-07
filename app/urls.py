from django.contrib import admin
from django.urls import path, include
from .views import lista_produtos, detalhes, compra,cancelar_compra,trabalhe_conosco, show_comentario,caracteristicas,categoria
from .views import sobre_produto,anuncios,fornecedores_produto,garantia_produto, forum_de_duvidas
urlpatterns = [
       path('', lista_produtos, name='listaprodutos'),

       path('trabalhe_conosco/', trabalhe_conosco, name='trabalhe_conosco'),
       path('detalhes/<slug:slug>/', detalhes, name='detalhes'),
       path('caracteristicas/<slug:slug>/<int:id>/', caracteristicas, name='caracteristicas'),
       path('comentario/<slug:slug>/<int:id>/', show_comentario, name='show_comentario'),
       path('comprar/<slug:slug>/', compra, name='comprar'),
       path('anuncios/<slug:slug>/', anuncios, name='anuncios'),
       path('sobre_produto/<slug:slug>/', sobre_produto, name='sobre_produto'),
       path('garantia_produto/<slug:slug>/', garantia_produto, name='garantia_produto'),
       path('fornecedores_produto/<slug:slug>/', fornecedores_produto, name='fornecedores_produto'),
       path('forum_de_duvidas/<slug:slug>/', forum_de_duvidas, name='forum_de_duvidas'),
       path('cancelar_compra/<slug:slug>/', cancelar_compra, name='cancelar_compra'),
       path('categoria/<slug:slug>/', categoria, name='categoria'),
]
