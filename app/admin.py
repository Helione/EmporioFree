from django.contrib import admin
from .models import Produto, Compra, Anuncio,Comentario
# Register your models here.

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'categoria']
    search_fields = ['nome', 'slug', 'categoria']
    prepopulated_fields = {'slug':('nome',)}

admin.site.register(Produto, ProdutoAdmin)
admin.site.register([Compra,Anuncio,Comentario])