from django import template

register = template.Library()


@register.filter(name='cut_text')
def cut_text(value, key):
    if len(value) >= key:
        value = str(value)[:key] + '...'
    return value
