from django import template

register = template.Library()

@register.filter()
def capitalize(arg):
    return arg.capitalize()