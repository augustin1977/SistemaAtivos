from usuarios.models import *
from usuarios.views import *
from equipamentos.views import *
from equipamentos.models import *
from notas.models import *
import pytz
import datetime

def run():
    print("configurando o sistema")
    print("Criando tipos de usuarios")
    tipos={'admin','user','superuser','especialuser'}
    for tipo in tipos :
        usuarios=Tipo.objects.filter(tipo=tipo)
        if len(usuarios)==0:
            tipo=Tipo(tipo=tipo)
            tipo.save()
        else:
            print(f"Usuario '{tipo}' ja existe!")
    print("Verificando usuário do sistema")
    if len(Usuario.objects.filter(nome="System"))==0:
        print("Criando usuario do sistema")
        senha=gera_senha(12)
        usuario=Usuario(nome='System', email='ericaugustin@ipt.br',tipo=Tipo.objects.get(tipo='admin'),primeiro_acesso=1, senha=senha)
        usuario.save()
    # importanto dados dos arquivos CSV
    print("Criando arvore de falhas")
    disciplinas=['Elétrica','Mecânica','Hidraulica',"Civil",'Eletrônica','Informática','Geral','Outros']
    cadastradas=Disciplina.objects.all()

    for disciplina in disciplinas:
        print(f"Cadastrando a disciplina {disciplina}")
        if disciplina not in cadastradas:
            d=Disciplina(disciplina=disciplina)
            d.save()
    

    eletrica=["Defeito Painel",'Problema no cabo Alimentação',"Sem energia","Fusivel Queimado","Falha Motor","Preventiva",
              'Falha na botoeira','Falha no inversor','Falha Disjuntor','Resistencia Queimada','outros']
    mecanica=['Quebra de componente', 'Falha estrutural','Travamento','Entupimento','Lubrificação','vazamento','calibração',
              'Preventiva','Ajustes','outros']
    hidraulica=['Mangueira vazando/rompida','vazamento','falta de oleo','baixa pressão de óleo','Manômetro','Entupimento','preventiva',
                'Calibração','Sensor vazão','outros']
    civil=['Problema Base fixação','Chummbar equipamento','Pitura','outros']
    TI=['Erro sistema Operacional',"computador não liga/inicia",'Tela Azul','Sistema travado','Erro comunicação','calibração','outros']
    outros=["Outros", 'Falta energia','Equipamento sem componentes']
    geral=['Falha geral', 'problema não identificado','outros']
    eletronica=['Placa queimada/defeito','botão/ botoeira com defeito','Falha sensor','PLC travado/queimado','Preventiva','Calibração','outros' ]
    
    disciplinas={'Elétrica':eletrica,'Mecânica':mecanica,'Hidraulica':hidraulica,"Civil":civil,'Eletrônica':eletronica,'Informática':TI,'Geral':geral,'Outros':outros}
    print("Cadastrando modos de falha")
    for disciplina in disciplinas:
        d=Disciplina.objects.get(disciplina=disciplina)
        modos=Modo_Falha.objects.filter(disciplina=disciplina)
        for i in disciplinas[i]:
            if i not in modos:
                m=Modo_Falha(disciplina=disciplina,Modo_Falha=i.capitalize() )
                m.save()
                print(f"Cadastrando o modo de falha {disciplina[i]}.{i}")


    print("Bancos de dados  básicos criados")
    print("iniciando migração dos dados dos arquivos 'csv'")
    print("Importanto locais de instalação")
    # criando local de instalação descarte
    local= Local_instalacao.objects.filter(laboratorio='Descarte')
    if len(local)==0:
        local=Local_instalacao(laboratorio='Descarte',
                            predio="Descarte",
                            piso="Descarte",
                            sala="Descarte",
                            armario="Descarte",
                            prateleira="Descarte",
                            apelido_local="Descarte"   )
        local.save()
    caminho=os.path.join(BASE_DIR,"banco Migrado",'local.csv')
    try:
        arquivo=open(caminho,'r')
        dados=arquivo.readline()
        dados=arquivo.readline()
        conteudo=[]
        while(dados):
            dado=dados.split(";")
            piso=None
            sala=None
            armario=None
            prateleira=None
            apelido_local=None
            predio=None
            if not dado[0]=="":
                conteudo.append(dado)
                predio=dado[0]
                if not dado[1]=="":
                    piso= dado[1]
                if not dado[2]=="":
                    sala="Sala "+dado[2]
                if not dado[3]=="":
                    armario=dados[3]
                if not dado[4]=="":
                    prateleira=dados[4]
                if not dado[5]=="" and dado[5]!="\n":
                    apelido_local=dados[5] 
                buscalocal=Local_instalacao.objects.filter(laboratorio='LPM',
                    predio=predio,
                    piso=piso,
                    sala=sala,
                    armario=armario,
                    prateleira=prateleira,
                    apelido_local=apelido_local)
                if len(buscalocal)==0:

                    local=Local_instalacao(laboratorio='LPM',
                        predio=predio,
                        piso=piso,
                        sala=sala,
                        armario=armario,
                        prateleira=prateleira,
                        apelido_local=apelido_local   )
                    print(predio,piso,sala,armario,prateleira,apelido_local)
                    local.save()
            dados=arquivo.readline()
        arquivo.close()
    except Exception as err:
        print("Erro ao extrair dados do local instalação", err)
    print ("Importando tipos de equipamento")
    # verifica se existe o tipo outros
    outros=Tipo_equipamento.objects.get(nome_tipo="Outros")
    if outros:
        outro=Tipo_equipamento(nome_tipo="Outros",sigla="OUT",descricao_tipo="Outros equipamentos")
        outro.save()
    caminho=os.path.join(BASE_DIR,"banco Migrado",'tipo.csv')
    arquivo=open(caminho,'r',encoding='utf-8')
    dados=arquivo.readline()
    dados=arquivo.readline()
    siglas=[]
    conteudo=[]
    tipos=Tipo_equipamento.objects.all()
    for tipo in tipos:
        siglas.append(tipo.sigla)
    while(dados):
        dado=dados.split(";") 
        conteudo.append(dado)
        temp=dado[0].capitalize()
        if dado[0]!="":
            buscatipo=Tipo_equipamento.objects.filter(nome_tipo=temp)
            if len(buscatipo)==0:
                sigla,siglas=funcoesAuxiliares.fazlista(dado[0],siglas)
                tipo=Tipo_equipamento(nome_tipo=temp, sigla=sigla)
                print(tipo)
                tipo.save()
        dados=arquivo.readline()
    arquivo.close()
    
    print("Importanto cadastro de  Fabricantes")
    caminho=os.path.join(BASE_DIR,"banco Migrado",'fabricante.csv')
    arquivo=open(caminho,'r')
    dados=arquivo.readline()
    dados=arquivo.readline()
    while(dados):
        dado=dados.split(";") 
        tmp=dado[0].capitalize().strip()
        if dado[0]!="" and len(dado[0])>=3:
            buscaFabricante= Fabricante.objects.filter(nome_fabricante=tmp)
            if len(buscaFabricante)==0:  
                fabricante=Fabricante(nome_fabricante=tmp,dados_adicionais=dado[1])
                print(fabricante)
                fabricante.save()
        dados=arquivo.readline()
    arquivo.close()
    print("importanto cadastro Equipamentos")
    caminho=os.path.join(BASE_DIR,"banco Migrado",'equipamentos.csv')
    arquivo=open(caminho,'r')
    dados=arquivo.readline()
    dados=dados.split(";")

    cont=0
    while(dados):
        dados=arquivo.readline()
        dado=dados.split(";") 
        if (dado[0]!="" and len(dado[0])>=2):
            cont+=1
            usuario=Usuario.objects.filter(nome="System")
            local=Local_instalacao.objects.filter(laboratorio=dado[0],predio=dado[1])
            tipo=Tipo_equipamento.objects.filter(nome_tipo=dado[6].capitalize())
            fabricante=Fabricante.objects.filter(nome_fabricante__contains=dado[7])
            eqptos=Equipamento.objects.filter(tipo_equipamento=tipo[0],ativo=True)
            numero=len(eqptos)+1
            #print(usuario,local,tipo,fabricante,eqptos,numero)
            if len(fabricante)==0:
                fabricante=[None]
            if len(local)==0:
                local=[None]
            codigo=f'{tipo[0].sigla.upper()}{numero:03d}'
            BR = pytz.timezone(TIME_ZONE)
            hoje=BR.localize( datetime.datetime.now())
            if len(dado[15])>2:
                tensao=dado[15]
            if len(dado[15])>2:
                tensao+="/"+dado[16]
                tensao+="V"
            try:
                valor=float(dado[9])
            except:
                valor=0.01    
            if len(dados[17])>2:
                tensao+=f"-{dados[17]} - {dado[18]}"     
            if "/" in dado[25]:
                try:
                    data_compra  = datetime.strptime(dado[25], "%d/%m/%Y")
                except:
                    data_compra=BR.localize(datetime.datetime(year=1899,month=1,day=1))
            else:
                try:
                    ano=int(dado[25])
                    data_compra=BR.localize(datetime.datetime(year=ano,month=1,day=1))
                except:
                    data_compra=BR.localize(datetime.datetime(year=1899,month=1,day=1))
            buscaequipamento=Equipamento.objects.filter(nome_equipamento=dado[4].capitalize(),fabricante=fabricante[0],local=local[0],modelo=dado[19],
                        tipo_equipamento=tipo[0],data_compra=data_compra,patrimonio=dado[28],
                        codigo=codigo, custo_aquisição=valor,custo_aquisição_currency="BRL",responsavel=dado[12].capitalize(),
                        potencia_eletrica=dado[13]+dado[14],nacionalidade=dado[24],data_ultima_atualizacao= hoje,
                        tensao_eletrica=tensao,projeto_compra=dado[26],especificacao=dado[20]+" "+dado[22],
                        outros_dados=dado[29])
            if len(buscaequipamento)==0:
                equipamento=Equipamento(nome_equipamento=dado[4].capitalize(),fabricante=fabricante[0],local=local[0],modelo=dado[19],
                        tipo_equipamento=tipo[0],data_compra=data_compra,usuario=usuario[0],patrimonio=dado[28],
                        codigo=codigo, custo_aquisição=valor,custo_aquisição_currency="BRL",responsavel=dado[12].capitalize(),
                        potencia_eletrica=dado[13]+dado[14],nacionalidade=dado[24],data_ultima_atualizacao= hoje,
                        tensao_eletrica=tensao,projeto_compra=dado[26],especificacao=dado[20]+" "+dado[22],
                        outros_dados=dado[29],ativo=True)
                print(equipamento)
                equipamento.save()
    arquivo.close()
