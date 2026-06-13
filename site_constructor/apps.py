from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_pages(sender, **kwargs):
    """Создаёт страницы по умолчанию если их нет."""
    from site_constructor.models import SitePage
    defaults = [
        ('services',  'Услуги',          'services',  0),
        ('team',      'Команда',         'team',      1),
        ('portfolio', 'Портфолио',       'portfolio', 2),
        ('news',      'Новости и акции', 'news',      3),
        ('products',  'Товары',          'products',  4),
    ]
    for page_type, nav_label, slug, order in defaults:
        SitePage.objects.get_or_create(
            page_type=page_type,
            defaults={
                'nav_label':  nav_label,
                'slug':       slug,
                'order':      order,
                'is_visible': True,
            },
        )


class SiteConstructorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'site_constructor'
    verbose_name = 'Настройки сайта'

    def ready(self):
        post_migrate.connect(create_default_pages, sender=self)