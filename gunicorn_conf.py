# gunicorn.conf.py

import multiprocessing


bind = "10.11.39.220:8000"
logfile = "/home/admin/logs/gunicorn.log"
workers = multiprocessing.cpu_count() * 2 + 1  # Número de workers para processamento
#timeout = 120  # Tempo limite de conexão em segundos

# Configurações para servir arquivos estáticos
def on_starting(server):
    server._app_holder.settings.STATIC_ROOT = '/caminho/para/pasta/estatica/'

    from django.core.management import call_command
    call_command('collectstatic', interactive=False)

    from whitenoise import WhiteNoise
    server.application = WhiteNoise(server.application, root=server._app_holder.settings.STATIC_ROOT)

# Outras configurações do Gunicorn...
