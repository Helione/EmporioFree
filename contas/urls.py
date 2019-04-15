from django.urls import path
from .views import register,carrinho, painel, editar, editar_senha, recuperar_senha

urlpatterns = [
    path('cadastrar/', register, name='cadastrar'),
    path('recuperar_senha/', recuperar_senha, name='recuperar_senha'),
    path('carrinho/', carrinho, name='carrinho'),
    path('painel/', painel, name='painel'),
    path('editar/', editar, name='editar'),
    path('editar_senha/', editar_senha, name='editar_senha'),

]
