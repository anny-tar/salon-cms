from django.apps import AppConfig


class SpecialistsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'specialists'
    verbose_name = 'Специалисты'

    def ready(self):
        import specialists.signals