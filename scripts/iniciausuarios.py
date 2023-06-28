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
        nome_arquivo=os.path.join(BASE_DIR,"banco Migrado",'Lista_LPM.txt') # abre o arquivo onde estão os dados do usuários
        
        arquivo=open(nome_arquivo,"r") # abre o oarquivo e pula as primieras linhas de cabeçalho
        linha=arquivo.readline()
        linha=arquivo.readline()
        linha=arquivo.readline()
        linha=arquivo.readline()
        i=0
        while(linha):
            linha=arquivo.readline().strip() # Retira espaços indesejados
            vetor=linha.split('\t') # cria o vetor com os valores
            if vetor[0]:
                remetentes[vetor[0]]=vetor[1]
            i+=1 # conta numero de linhas lidas
        arquivo.close()
    except Exception as erro:
        print(erro) # imp´rime o erro em caso de erro
    pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$" # Padrão para verificar se o email é um valor válido
    tipo=Tipo.objects.filter(tipo="user")
    sis=Usuario.objects.get(nome='System') # pega o usuario System
    #print(Tipo[0])
    remetentes={"Eric Augustin":"ericaugustin@gmail.com","Eric Augustin":"ericaugustin@hotmail.com"}
    for nome in remetentes: # itera cada nome no dicionário remetentes
        if nome and remetentes[nome]: # verifica se no dicionario está completa como nome e email
            if re.search(pattern, remetentes[nome]): # verifica se o e-mail é valido
                senha=gera_senha(12) # gera uma senha aleatoria de 12 digitos 
                senha_cripto=sha256(senha.encode()).hexdigest() # criptografa a senha usado sha256
                if len(Usuario.objects.filter(email=remetentes[nome]))==0: # verifica se o email ja está no banco de dados
                    usuario=Usuario(nome=nome,chapa=0,email=remetentes[nome],senha=senha_cripto,tipo=tipo[0],primeiro_acesso=True,ativo=True)
                    usuario.save() # caso o usuario não exista, cadastra o usuario e salva no banco
                    
                    Log.cadastramento(usuario,sis,'us') # grava o log de cadastro no sistema
                    print(usuario,"-",remetentes[nome],'-',senha) # imprime usuario, email e senha na tela
                    # texto do email em HTML
                    conteudo_html=f"""<html>
                                <head></head>
                                <body>
                                    <h2>Olá {nome}!</h2>
                                    <p>Seu cadastro no sistema de Gestão de Ativos do LPM foi concluído com sucesso.</p>
                                    <p>Os dados para login são:</p>
                                    <p>Seu nome de usuário: {remetentes[nome]}</p>
                                    <p>Sua senha provisória: {senha}</p>
                                    <p>O link do sistema é: <a href="http://gestaoativosma.ad.ipt.br/">gestaoativosma.ad.ipt.br </p>
                                    <p>Obrigado!</p>
                                </body>
                                </html>"""
                    # texto plain do email caso falhe o HTML
                    conteudo_plain=f"Seu cadastro foi concluido com sucesso, sua senha é {senha}"
                    try:
                        # envia o email 
                        send_mail(subject='Cadastro no Sistema de Gestão de Ativos',message=conteudo_plain,
                            from_email="gestaodeativos@outlook.com.br",recipient_list=[usuario.email,info_email['email']],
                            html_message=conteudo_html)  
                        #time.sleep(random.randint(1,2)+random.randint(0,5))
                    except Exception as erro:
                        print("#######Erro no envio do email############")
                        print(erro) # em caso de erro imprime o erro
                else:
                    print(f"email {remetentes[nome]} já existe") # caso o usuário ja exista imprime nome do usuario e informa que ja existe
            else:
                print("##################Email incorreto##################")
        else:
            print("##################Errro##################")