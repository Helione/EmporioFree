from django.db import models
from app.models import Produto
from django.forms import modelformset_factory
# Create your models here.



class CartItemManager(models.Manager):
    def add_item(self, chave_carrinho, produto):
        if self.filter(chave_carrinho=chave_carrinho, produto=produto).exists():
            created = False
            cart_item = self.get(chave_carrinho=chave_carrinho, produto=produto)
            cart_item.quantidade = cart_item.quantidade +1
            cart_item.save()
        else:
            created = True
            cart_item = CartItem.objects.create(chave_carrinho=chave_carrinho, produto=produto, preco=produto.preco)

        return cart_item, created

class CartItem(models.Model):

    chave_carrinho = models.CharField('Chave do Carrinho', max_length=40, db_index=True)
    produto=models.ForeignKey(
        Produto, verbose_name='Produto',
                on_delete=models.CASCADE,
                related_name='cartitem'
    )
    quantidade = models.PositiveIntegerField('Quantidade',default=1)
    preco = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    objects= CartItemManager()

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens dos Carrinhos'
        unique_together = (('chave_carrinho', 'produto'),)

    def __str__(self):
        return '{} [{}]'.format(self.produto, self.quantidade)