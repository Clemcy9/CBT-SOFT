from django import template
register = template.Library()

@register.filter()
def ascend(arg): 
    return arg.sort()
