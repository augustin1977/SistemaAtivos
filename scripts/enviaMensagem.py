from usuarios.models import *
from usuarios.enviar_email import *
import time
def envia_comunicado_todos(assunto,mensagem):
    usuarios= Usuario.objects.all()
    for usuario in usuarios:
        email=usuario.email
        try:
            enviar_email(assunto,mensagem,[email])
        except Exception as e:
           print(f"Erro ao enviar mensagem ao usuario -> {usuario}")
           print(e) 
        time.sleep(5)
        

        