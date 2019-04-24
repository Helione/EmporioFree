from django.db import models
from django.urls import reverse
from django.conf import settings
# Create your models here.

class ProdutoManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains = query)| \
            models.Q(description__icontains = query) #icontains -- busca no nome e descrição
    )

class Produto(models.Model):
    nome= models.CharField('Nome',max_length=30)
    slug = models.SlugField('Atalho')  # SlugField--Adiciona urls mais explicativas
    preco = models.DecimalField('Preço',max_digits=8, decimal_places=4)
    descricao = models.TextField('Descrição Simples', blank=True)
    quantidade = models.IntegerField('Quantidade')
    categoria = models.CharField('Categoria',max_length=10)
    foto = models.ImageField('Foto', upload_to='midia', null=True, blank=True)

    start_date = models.DateField(
        'Data de Início', null= True, blank=True  #Null-- A nível de BD pode ser nulo
    )

    created_at = models.DateTimeField('Criado em ', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em ', auto_now=True)

    objects = ProdutoManager()

    def __str__(self):
        return self.nome

    def get_slug_field(self):
        return reverse('detalhes', args = [self.slug])

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']

class Compra(models.Model):
    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
                                on_delete=models.CASCADE,
                                related_name= 'compras'
    )
    produto = models.ForeignKey(
        Produto, verbose_name = 'Produto',
                on_delete=models.CASCADE,
                related_name = 'compras'
    )
    status = models.IntegerField(
        'Situação', choices = STATUS_CHOICES, default= 1, blank= True
    )

    created_at = models.DateTimeField('Criado em ', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em ', auto_now=True)

    def active(self): # ativar o usuário
        self.status = 1
        self.save()

    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        unique_together = (('user', 'produto'),)

class Anuncio(models.Model):
    produto = models.ForeignKey(Produto, verbose_name='Produto',
                                on_delete=models.CASCADE)
    title= models.CharField('Título', max_length=100)
    conteudo=models.TextField('Conteúdo')

    created_at = models.DateTimeField('Criado em ', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em ', auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural= 'Anúncios'
        ordering = ['-created_at']

class Comentario(models.Model):
    anuncio = models.ForeignKey(
        Anuncio, verbose_name='Anúncio',
        on_delete=models.CASCADE,
        related_name='comentário'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuário',
                             on_delete=models.CASCADE)
    comentario = models.TextField('Comentário')

    created_at = models.DateTimeField('Criado em ', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em ', auto_now=True)

    class Meta:
        verbose_name= 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']