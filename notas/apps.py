from django.apps import AppConfig
from django.db.models.signals import post_migrate

class NotasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notas"

    def ready(self):
            post_migrate.connect(init_data_bd, sender=self)

def init_data_bd(sender, **kwargs):
      pass