from django import template
register = template.Library()

@register.filter
def list_index(List, i):
    return List[int(i)]