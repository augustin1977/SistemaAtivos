from usuarios.models import *
from usuarios.views import *
from equipamentos.views import *
from equipamentos.models import *
from notas.models import *
from django.db.models import Q
import pytz
import datetime
import pandas as pd
import datetime
import os
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
    
    print("Cadastrando os modos de falha")
    for disciplina in disciplinas:
        d=Disciplina.objects.filter(disciplina=disciplina)
        modos=Modo_Falha.objects.filter(disciplina=d[0])
        for i in disciplinas[disciplina]:
            if i not in modos:
                print(f"Cadastrando o modo de falha {disciplina}.{i}")
                m=Modo_Falha(disciplina=d[0],modo_falha=i.capitalize() )
                m.save()  
    #Criando local descarte
    print("Cadastrando Local 'Descarte'")
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
    print("Cadastrando tipo 'Outros'")
    # verifica se existe o tipo de equipamento 'outros'
    outros=Tipo_equipamento.objects.get(nome_tipo="Outros")
    if outros:
        outro=Tipo_equipamento(nome_tipo="Outros",sigla="OUT",descricao_tipo="Outros equipamentos")
        outro.save()
    ##### Editar daqui pra baixo a migração dos dados######
    print("Bancos de dados  básicos criados")
    print("iniciando migração dos dados.")
   
    try:
        caminho=os.path.join(BASE_DIR,"banco Migrado",'NovoBanco','planilha_mestra_ativos_2.0v.exp.xlsm')
        df = pd.read_excel(caminho, sheet_name='input')
        df = df.fillna(0)

        tipos_variavel = {'Lab':str, 'Predio':int, 'Sala':str,'Piso':str, 'DetalheLocal':str, 'NomeEq':str, 'Apelido':str, 'Tipo':str, 'Cod_auto_raster':str, 'Fabricante':str,
                            'Moeda':str, 'Custo de aquisição':float, 'Agência financiadora':str, 'ID_grupo':str, 'Responsável':str, 'Potência elétrica':str, 
                            'Unidade potencia elétrica':str,'Tensão elétrica minima (V)':int, 'Tensão elétrica máxima (V)':int,
                            'Detalhe da alimentação elétrica (bivolt, trifásico, etc)':str, 'Outras alimentações (ar, água, etc)':str, 'Modelo':str, 
                            'Spec1':str, 'Unidade Spec1':str, 'Spec2':str, 'Unidade Spec2':str, 'Nacionalidade':str, 'Ano_compra':str, 'Projeto_financiador':str, 
                            'Sist_patrimonio':str, 'Patrimonio':str, 'Finalidade':str, 'inter_calib':str, 'Condição Equipamento':str,
                            'Data Atualização':str, 'Pasta_arquivos':str, 'OBS':str, 'Unnamed: 36':str, 'endereço':str}
        df = df.astype(tipos_variavel)	
        array_dados = df.values
        nomes_cabecalho = df.columns.tolist()
    except:
        print("erro de importação do arquivo excel")
        return 
    dados=[]
    # montando dados em um dicionário
    for linha in array_dados:
        dado={}
        for k,j in enumerate(nomes_cabecalho):
            dado[j]=linha[k]
        dados.append(dado)
    print("dados lido e carregados na memória")   
    print("Iniciando a gravação para o banco de dados")  
    for registro in dados:
        print(f"registrando Equipamento -> {registro['nomeEq']}")
        # Verificando se local de instalação existe e caso contrario fazendo o cadastro do local de instalação
        buscalocal=Local_instalacao.objects.filter(laboratorio=registro["Lab"],
                predio=registro['Predio'].capitalize(),
                piso=registro["piso"].capitalize(),
                sala=registro['sala'].capitalize())
        if len(buscalocal)==0:
            local=Local_instalacao(laboratorio='LPM',
                predio=registro['Predio'].capitalize(),
                piso=registro["piso"].capitalize(),
                sala=registro['sala'].capitalize(),
                armario=None,
                prateleira=None,
                apelido_local=registro['DetalheLocal'].capitalize()   )
            print(f"registrando Local Instalação-> {local}")
            local.save()
        else:
             local=buscalocal[0]
        # verificando se a sigla ja existe e caso contrario fazendo o cadastro da sigla
        nome_tipo=registro["Tipo"].capitalize()
        buscatipo=Tipo_equipamento.objects.filter(nome_tipo=nome_tipo.capitalize())
        siglas= list(Tipo_equipamento.objects.values_list('sigla',flat=True))
        if len(buscatipo)==0:
            sigla=funcoesAuxiliares.fazlista(nome_tipo,siglas)
            tipo=Tipo_equipamento(nome_tipo=nome_tipo.capitalize(), sigla=sigla)
            print(f"registrando Tipo Equipamento-> {tipo}")
            tipo.save()
        else: 
            tipo=buscatipo[0]
        buscaFabricante= Fabricante.objects.filter(nome_fabricante=registro['Fabricante'].capitalize())
        if len(buscaFabricante)==0:  
            fabricante=Fabricante(nome_fabricante=registro['Fabricante'].capitalize())
            print(f"registrando Fabricante-> {fabricante}")
            fabricante.save()
        else:
             fabricante=buscaFabricante[0]
        
        usuario=Usuario.objects.filter(nome="System")[0]
        eqptos=Equipamento.objects.filter(tipo_equipamento=tipo,ativo=True)
        numero=len(eqptos)+1
        codigo=f'{tipo.sigla.upper()}{numero:03d}'
        BR = pytz.timezone(TIME_ZONE)
        hoje=BR.localize( datetime.datetime.now())
        # codificado até aqui
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
                filtro1=Q(disciplina='Mecânica')
                filtro2=Q(disciplina='Geral')
                filtro3=Q(disciplina='Outros')
                modos=Modo_Falha.objects.filter(filtro1|filtro2|filtro3)
                for modo in modos:
                    m=Modo_falha_equipamento(equipamento=equipamento,modo_falha=modo)
                    m.save()
                    print(modo,m)
                if equipamento.potencia_eletrica and equipamento.tensao_eletrica:
                    modos=Modo_Falha.objects.filter(disciplina='Elétrica')
                    for modo in modos:
                        m=Modo_falha_equipamento(equipamento=equipamento,modo_falha=modo)
                        m.save()
                        print(modo,m)

        
    arquivo.close()
