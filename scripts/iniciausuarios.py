import os
import re
from usuarios.views import *
from usuarios.models import *
from cadastro_equipamentos.settings import BASE_DIR
import time
import random
from django.core.mail import send_mail
from info_email import *
def run():
    print("importando dados do excel!")
    remetentes={}
    try:
        nome_arquivo=os.path.join(BASE_DIR,"banco Migrado",'Lista_LPM.txt')
        
        arquivo=open(nome_arquivo,"r")
        linha=arquivo.readline()
        linha=arquivo.readline()
        linha=arquivo.readline()
        linha=arquivo.readline()
        i=0
        while(linha):
            linha=arquivo.readline().strip()
            vetor=linha.split('\t')
            if vetor[0]:
                remetentes[vetor[0]]=vetor[1]
            i+=1
        arquivo.close()
    except Exception as erro:
        print(erro)
    pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    tipo=Tipo.objects.filter(tipo="user")
    #print(Tipo[0])
    remetentes={"Eric Augustin":"ericaugustin@gmail.com"}
    for nome in remetentes:
        if nome and remetentes[nome]:
            if re.search(pattern, remetentes[nome]):

                senha=gera_senha(12)
                senha_cripto=sha256(senha.encode()).hexdigest()
                if len(Usuario.objects.filter(email=remetentes[nome]))==0:
                    usuario=Usuario(nome=nome,chapa=0,email=remetentes[nome],senha=senha_cripto,tipo=tipo[0],primeiro_acesso=True,ativo=True)
                    usuario.save()
                    sis=Usuario.objects.get(nome='System')
                    Log.cadastramento(usuario,sis,'us')
                    print(usuario,"-",remetentes[nome],'-',senha)
                    
                    conteudo_html=f"""<html>
                                <head></head>
                                <body>
                                    <h2>Olá {nome}!</h2>
                                    <p>Seu cadastro no sistema de Gestão de Ativos do LPM foi concluído com sucesso.</p>
                                    <p>Os dados para login são:</p>
                                    <p>Seu nome de usuário: {remetentes[nome]}</p>
                                    <p>Sua senha provisória: {senha}</p>
                                    <p>Obrigado!</p>
                                </body>
                                </html>"""
                    conteudo_plain=f"Seu cadastro foi concluido com sucesso, sua senha é {senha}"
                    try:
                        send_mail(subject='Cadastro no Sistema de Gestão de Ativos',message=conteudo_plain,
                            from_email="gestaodeativos@outlook.com.br",recipient_list=[usuario.email,info_email['email']],
                            html_message=conteudo_html)  
                        #time.sleep(random.randint(1,2)+random.randint(0,5))
                    except Exception as erro:
                        print("#######Erro no envio do email############")
                        print(erro)
                else:
                    print(f"email {remetentes[nome]} já existe")
            else:
                print("##################Email incorreto##################")
        else:
            print("##################Errro##################")