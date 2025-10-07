from django.apps import AppConfig

class ApplicationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.applications' 
    label = 'applications'

    def ready(self):
        # Import models to ensure they're registered
        from . import models