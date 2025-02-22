from django.apps import AppConfig

class AppsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps'
    label = 'apps'
    def ready(self):
        print("Hello")
