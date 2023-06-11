from django import template
import random

register = template.Library()

@register.filter()
def randomize(arg):
    aux = list(arg)[:]
    random.shuffle(aux)
    return aux