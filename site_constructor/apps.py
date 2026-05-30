from django.apps import AppConfig


class SiteConstructorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'site_constructor'
    verbose_name = 'Настройки сайта'