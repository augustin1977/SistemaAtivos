from django.apps import AppConfig
from django.db.models.signals import post_migrate

def inicializar_dados(sender,app_config, **kwargs):

    
    if app_config.name != "portifolio":
        return
    print("Executando carga inicial do sistema...")
    from scripts.carrega_dados_basicos import run
    run()
    print("Carga inicial concluída com sucesso!")


class CoreProjectConfig(AppConfig):
    name = "cadastro_equipamentos"
    verbose_name = "Cadastro dos Equipamentos"

    def ready(self):
        # conecta o sinal post_migrate a essa função
        post_migrate.connect(inicializar_dados)
