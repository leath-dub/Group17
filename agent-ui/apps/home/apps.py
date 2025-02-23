from django.apps import AppConfig
import threading
import sys

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.home'

    def ready(self):
        """Ensure event_listener runs when Django starts."""
        if 'migrate' in sys.argv or 'makemigrations' in sys.argv:
            return

        from apps.home.startup import event_listener
        server_thread = threading.Thread(target=event_listener, daemon=True)
        server_thread.start()
