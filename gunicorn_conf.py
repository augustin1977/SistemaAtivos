# gunicorn.conf.py

import multiprocessing
#import os
#from cadastro_equipamentos.settings import BASE_DIR



bind = "10.11.39.220:8000"
logfile = "/home/admin/gunicorn.log"
workers = multiprocessing.cpu_count() * 2 - 1  # Número de workers para processamento
#timeout = 120  # Tempo limite de conexão em segundos
chdir = "/home/admin/SistemaAtivos/SistemaAtivos"

#