from django.apps import AppConfig

class SchoolErpAiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "school_erp_ai"

    def ready(self):
        from . import admin  # 👈 FORCE LOAD
