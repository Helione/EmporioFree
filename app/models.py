from django.db import models
from django.urls import reverse
from django.conf import settings
# Create your models here.
from app.mail import send_mail_template

class ProdutoManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains = query)| \
            models.Q(description__icontains = query) #icontains -- busca no nome e descrição
    )

class Produto(models.Model):
    nome= models.CharField('Nome',max_length=100)
    slug = models.SlugField('Atalho')  # SlugField--Adiciona urls mais explicativas
    preco = models.DecimalField('Preço',max_digits=8, decimal_places=2)
    descricao = models.TextField('Descrição Simples', blank=True)
    quantidade = models.IntegerField('Quantidade')
    categoria = models.ForeignKey(
                   'Categoria',
                   on_delete=models.CASCADE,
    )

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

class Caracteristicas(models.Model):

    produto = models.ForeignKey(
        Produto, verbose_name='Produto',
                on_delete=models.CASCADE,
                related_name='caracteristicas'
    )
    inftecnica = models.TextField('Informação Técnica')
    infalergia = models.TextField('Informação sobre alergênicos', blank=True, null=True)
    infnutricional = models.TextField('Informação Nutricional', blank=True, null=True)
    escolha = models.TextField('Por que escolher esse produto?',blank=True,null=True)
    marca = models.CharField('Sobre a Marca',max_length=50)
    ingredientes = models.TextField('Ingredientes',blank=True, null=True)
    recomendacao = models.TextField('Recomendação de consumo',blank=True, null=True)

    created_at = models.DateTimeField('Criado em ', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em ', auto_now=True)

    def __srt__(self):
        return self.produto

    class Meta:
        verbose_name ='Característica'
        verbose_name_plural = 'Características'


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


    def __str__(self):
        return self.user

    def active(self): # ativar o usuário
        self.status = 1
        self.save()

    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        unique_together = (('user', 'produto'),)

def post_save_compra(instance,created, **kwargs):
    if created:
        subject = instance.produto
        context ={
            'compra':instance
        }
        template_name ='compra_mail.html'
        compras= Compra.objects.filter(
            produto=instance.produto, status=1 #instancia diretamente do campo
        )
        for compra in compras:
            recipient_list =[compra.user.email]
            send_mail_template(subject,template_name,context,recipient_list)
models.signals.post_save.connect(
    post_save_compra, sender=Compra,#conexão com quem irá enviar
    dispatch_uid='post_save_compra' #identificando esse sinal para ser enviado uma única vez
)

class Detalhe(models.Model):
    produto=models.ForeignKey(
        Produto, verbose_name='Produto',
                on_delete=models.CASCADE,
                related_name='detalhes'
    )
    created_at = models.DateTimeField('Criado em ', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em ', auto_now=True)

    def __str__(self):
        return self.produto

    class Meta:
        verbose_name = 'Detalhe'
        verbose_name_plural = 'Detalhes'

class Comentario(models.Model):
    detalhe = models.ForeignKey(
        Detalhe, verbose_name='Detalhe',
                on_delete=models.CASCADE,
                related_name='comentarios'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
                             on_delete=models.CASCADE,
                             related_name='comentarios'
    )

    comentario = models.TextField('Comentário')

    created_at = models.DateTimeField('Criado em ', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em ', auto_now=True)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name= 'Comentário'
        verbose_name_plural = 'Comentários'

class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')

    def __str__(self):
        return self.nome

    def get_slug_field(self):
        return reverse('categoria', args = [self.slug])

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

