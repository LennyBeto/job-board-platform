from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authentication'
    label = 'authentication'
    
    def ready(self):
        # Import models to ensure they're registered
        from . import models