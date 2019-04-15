
from django.template import Library
register = Library()
Library.assignment_tag = Library.simple_tag



from app.models import Compra

@register.inclusion_tag('templatetags/my_produtos.html')
def my_produtos(user):
    compras = Compra.objects.filter(user=user)
    return  {'compras' : compras}

@register.assignment_tag
def load_my_produtos(user):
    return Compra.objects.filter(user=user)