from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Универсальный доступ к словарю по ключу в шаблоне: dict|get_item:key"""
    if not dictionary:
        return None
    return dictionary.get(key)