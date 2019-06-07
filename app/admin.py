from django.contrib import admin
from .models import Produto, Compra,Comentario,Detalhe,Caracteristicas,Categoria
# Register your models here.

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'categoria']
    search_fields = ['nome', 'slug', 'categoria']
    prepopulated_fields = {'slug':('nome',)}

class CaracteristicasAdmin(admin.ModelAdmin):

    list_display = ['produto', 'marca']
    search_fields = ['produto', 'inftecnica']
    list_filter = ['created_at']

class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('produto',)}
    search_fields = ['produto']

admin.site.register(Produto, ProdutoAdmin)
admin.site.register([Compra, Comentario, Detalhe,Categoria])
admin.site.register(Caracteristicas,CaracteristicasAdmin)
