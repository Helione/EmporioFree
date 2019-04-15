import re
from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        'Nome de Usuário', max_length=30, unique=True,
        validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
             'O Nome de usuário só pode conter letras e dígitos sem espaços ou os'
             ' seguintes caracteres: @/./+/-/_', 'invalid')]
    ) #usuário único
    email = models.EmailField('E-mail', unique=True) #email único
    name = models.CharField('Nome', max_length=100, blank=True) #opcional
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank=True,default=False) #Pode acessar o admin
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True) #auto_now_add -- quando o usuário for salvo irar ser com a data atual
                                                                                #auto_now-- atualiza toda vez que é salvo o valor
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] #Para ter conpatibilidade com atributos django

    def __str__(self):
        return self.name or self.username #Se houver nome retorna senão retorna username

    def get_short_name(self):
        return self.username  #Retorna username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class PasswordReset(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
                             on_delete=models.CASCADE,
                             related_name='resets'
     )
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em ', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)#verificar se não estar mudando para a mesma senha e fins de registro

    def __srt__(self):
        return '{0} em {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at']