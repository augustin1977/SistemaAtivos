from usuarios.models import *
from usuarios.views import *
from equipamentos.views import *
from equipamentos.models import *
from notas.models import *
from django.core.files import File
from django.db.models import Q
import pytz
import datetime
import pandas as pd
import datetime
import os
import shutil

def run():
    #abrindo dados arquivos
    print("Abrindo arquivo de dados dos usuarios!")
    