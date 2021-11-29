from django import template

from blog.models import Zastavka

register = template.Library()


@register.simple_tag(name='zas')
def get_zastavka():
    return Zastavka.objects.all()
