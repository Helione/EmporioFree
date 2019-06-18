from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView
from django.forms import modelformset_factory
from .models import CartItem
from django.contrib import messages
from app.models import Produto
# Create your views here.
class CreateCartItemView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        produto = get_object_or_404(Produto,slug=self.kwargs['slug'])
        if self.request.session.session_key is None:
            self.request.session.save()
        cart_item, created = CartItem.objects.add_item(
            self.request.session.session_key,produto
        )
        if created:
            messages.success(self.request, 'Produto adicionado com sucesso')
        else:
            messages.success(self.request, 'Produto atualizado com sucesso')

        return reverse('cart_item')

class CartItemView(TemplateView):

    template_name = 'carrinho.html'

    def get_context_data(self, **kwargs):
        context = super(CartItemView, self).get_context_data(**kwargs)
        CartItemFormSet = modelformset_factory(
            CartItem, fields=('quantidade',), can_delete=True, extra=0
        )
        session_key = self.request.session.session_key
        if session_key:
            context['formset'] = CartItemFormSet(
                queryset=CartItem.objects.filter(chave_carrinho=session_key)
            )
        else:
            context['formset']= CartItemFormSet(queryset=CartItem.objects.none())
        return context


create_cartitem = CreateCartItemView.as_view()
cart_item = CartItemView.as_view()

