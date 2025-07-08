from django.apps import AppConfig
from . import heartbeat
import os

class ClientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "clients"

    def ready(self):
        if os.environ.get("RUN_MAIN") == "true":
            heartbeat.start()