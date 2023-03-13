from usuarios.models import *
from usuarios.views import *
from equipamentos.views import *
from equipamentos.models import *


def run():
    print('configurando o sistema')
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
        usuario=Usuario(nome='System', email='ericaugustin@ipt.br',tipo=Tipo.objects.get(tipo='superuser'),primeiro_acesso=1, senha=senha)
    # importanto dados dos arquivos CSV
    print("Bancos de dados criados")
    print("iniciando migração dos dados dos arquivos 'csv'")
    print("Importanto locais de instalação")
    caminho=os.path.join(BASE_DIR,"banco Migrado",'local.csv')
    arquivo=open(caminho,'r', encoding='utf-8')
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
                local.save()
        dados=arquivo.readline()
    arquivo.close()
    print ("Importando tipos de equipamento")
    caminho=os.path.join(BASE_DIR,"banco Migrado",'tipo.csv')
    arquivo=open(caminho,'r', encoding='utf-8')
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
        print(dado[0], len(dados[0]))
        if dado[0]!="":
            
            buscatipo=Tipo_equipamento.objects.filter(nome_tipo=dado[0])
            if len(buscatipo)==0:
                sigla,siglas=funcoesAuxiliares.fazlista(dado[0],siglas)
                tipo=Tipo_equipamento(nome_tipo=dado[0], sigla=sigla)
                tipo.save()
        dados=arquivo.readline()
    arquivo.close()
    
    print("Importanto cadastro de  Fabricantes")
    caminho=os.path.join(BASE_DIR,"banco Migrado",'fabricante.csv')
    arquivo=open(caminho,'r', encoding='utf-8')
    dados=arquivo.readline()
    dados=arquivo.readline()
    conteudo=[]
    while(dados):
        dado=dados.split(";") 
        if dado[0]!="" and len(dado[0])>=3:
            buscaFabricante= Fabricante.objects.filter(nome_fabricante=dado[0].capitalize())
            if len(buscaFabricante)==0:
                conteudo.append(dado)   
                fabricante=Fabricante(nome_fabricante=dado[0].capitalize())
                fabricante.save()
        dados=arquivo.readline()
    arquivo.close()
    caminho=os.path.join(BASE_DIR,"banco Migrado",'equipamentos.csv')
    arquivo=open(caminho,'r', encoding='utf-8')

    dados=arquivo.readline()
    dados=dados.split(";")
    " - ".join(str(i)+str(d) for i,d in enumerate(dados))
    dados=arquivo.readline()
    cont=0
    while(dados):
        dado=dados.split(";") 
        if dado[0]!="" and len(dado[0])>=3:
            print(cont)
            cont+=1
            usuario=Usuario.objects.filter(nome="System")
            local=Local_instalacao.objects.filter(laboratorio=dado[0],predio=dado[1])
            tipo=Tipo_equipamento.objects.filter(nome_tipo=dado[6])
            fabricante=Fabricante.objects.filter(nome_fabricante__contains=dado[7])
            print=str(dados)
            if len(fabricante)==0:
                fabricante=[None]
            if len(local)==0:
                local=[None]
            if len(tipo)==0:
                tipo=Tipo_equipamento.objects.filter(nome_tipo='outros')
            eqptos=Equipamento.objects.filter(tipo_equipamento=tipo[0],ativo=True)
            numero=len(eqptos)+1
            codigo=f'{tipo[0].sigla.upper()}{numero:03d}'
            utc=pytz.UTC
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
            try:
                ano=int(dado[25])
            except:
                try :
                    data= datetime.
                    dado[25]
                except:
                    ano=1899
                
                data_compra=BR.localize(datetime.datetime(year=ano,month=1,day=1))
                


    #             equipamento=Equipamento(nome_equipamento=dado[4].capitalize(),fabricante=fabricante[0],local=local[0],modelo=dado[19],
    #                     tipo_equipamento=tipo[0],data_compra=data_compra,usuario=usuario[0],patrimonio=dado[28],
    #                     codigo=codigo, custo_aquisição=valor,custo_aquisição_currency="BRL",responsavel=dado[12].capitalize(),
    #                     potencia_eletrica=dado[13]+dado[14],nacionalidade=dado[24],data_ultima_atualizacao= hoje,
    #                     tensao_eletrica=tensao,projeto_compra=dado[26],especificacao=dado[20]+" "+dado[22],
    #                     outros_dados=dado[29])
    #             equipamento.save()
    #         dados=arquivo.readline()
    #     arquivo.close()
    #     return HttpResponse(conteudo)
    # elif request.GET.get('campo')=='arquivos':
    #     return HttpResponse("Não implementado")
        
    # return HttpResponse("Erro")
