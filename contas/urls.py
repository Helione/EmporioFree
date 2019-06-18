from django.urls import path
from .views import register,painel, editar, editar_senha, recuperar_senha, comprando

urlpatterns = [
    path('cadastrar/', register, name='cadastrar'),
    path('recuperar_senha/', recuperar_senha, name='recuperar_senha'),
    path('painel/', painel, name='painel'),
    path('editar/', editar, name='editar'),
    path('editar_senha/', editar_senha, name='editar_senha'),
    path('comprando/<slug:slug>/', comprando, name='comprando'),

]
