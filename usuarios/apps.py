from django.apps import AppConfig
from django.db.models.signals import post_migrate

# configurção da aplicação ususários
class UsuariosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "usuarios"

