from django.apps import AppConfig


class VisitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.visits'
    verbose_name = 'Murojaatlar'

    def ready(self):
        from . import signals  # noqa: F401
