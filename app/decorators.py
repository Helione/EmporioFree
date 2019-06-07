from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Produto, Compra

def compra_required(view_func):
    def _wrapper(request, *args, **kwargs):
        slug = kwargs['slug']
        produto = get_object_or_404(Produto, slug=slug)
        has_permission = request.user.is_staff
        if not has_permission:
            try:
                compra = Compra.objects.get(
                    user=request.user, produto=produto
                )
            except Compra.DoesNotExist:
                message = 'Desculpe, mas você não tem permissão para acessar esta página'
            else:
                if compra.is_approved():
                    has_permission = True
                else:
                    message = 'A sua compra ainda está pendente'
        if not has_permission:
            messages.error(request, message)
            return redirect('painel')
        request.produto = produto
        return view_func(request, *args, **kwargs)
    return _wrapper
