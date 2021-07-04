from django import template

register = template.Library()

@register.simple_tag
def define(val=None):
    return val

@register.filter
def remaining(num, mod):
    return range(mod - (num % mod))
