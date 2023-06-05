import os
import re
from usuarios.views import *
from usuarios.models import *
from cadastro_equipamentos.settings import BASE_DIR
def run():
    print("importando dados do excel!")
    #print(caminho)
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
    for nome in remetentes:
        if nome and remetentes[nome]:
            if re.search(pattern, remetentes[nome]):

                senha=gera_senha(12)
                senha_cripto=sha256(senha.encode()).hexdigest()
                if len(Usuario.objects.filter(email=remetentes[nome]))==0:
                    usuario=Usuario(nome=nome,chapa=0,email=remetentes[nome],senha=senha_cripto,tipo=tipo[0],primeiro_acesso=True,ativo=True)
                    usuario.save()
                    print(usuario,"-",remetentes[nome],'-',senha)
                    """try:
                        send_mail(subject='Cadastro no Sistema de Gestão de Ativos',
                            message=f"Foi gerado um cadastro para seu e-mail e sua senha é provisoria é {senha}",
                            from_email="gestaodeativos@outlook.com.br",recipient_list=[usuario.email,'gestaodeativos@ipt.br'])  
                    except:
                        print("#######Erro no envio do email############")"""
            else:
                print("##################Email incorreto##################")
        else:
            print("##################Errro##################")