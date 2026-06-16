from django import template
from site_constructor.models import Address

register = template.Library()


@register.simple_tag
def get_address(address_id):
    """Возвращает объект Address по ID (из settings секции map)."""
    if not address_id:
        return None
    try:
        return Address.objects.get(pk=address_id)
    except (Address.DoesNotExist, ValueError):
        return None