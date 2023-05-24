from django.apps import AppConfig
import traceback


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"