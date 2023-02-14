# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.staticfiles.views import serve
from django.http import HttpResponse
from .models import Usuario,Tipo,Equipamento,Material_consumo,Media,Fabricante
from django.shortcuts import redirect 
from hashlib import sha256
from cadastro_equipamentos import settings
from django.http import HttpResponse, Http404
from os import path
from cadastro_equipamentos.settings import BASE_DIR
from django.utils.encoding import smart_str
import re,os
from log.models import Log
from .forms import *
def home(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    # cria a view do login do usuário
    status=str(request.GET.get('status'))
    return render(request, "home.html", {'status':status})

def lista_equipamentos(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    usu=Usuario.objects.get(id=request.session.get('usuario'))
    print(f"{usu.nome} acessou Lista Equipamentos")
    equipamentos=Equipamento.objects.all()
    log=Log(transacao='eq',movimento='lt',usuario=usu,alteracao=f'{usu.nome} visualisou Lista equipamentos')
    log.save()
    return render(request, "exibirEquipamentos.html", {'equipamentos':equipamentos})

def exibirDetalheEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Detalhe Equipamentos")
    id=str(request.GET.get('id'))
    equipamento=Equipamento.objects.get(id=id)
    materiais=Material_consumo.objects.filter(equipamento__id=id)
    arquivos= Media.objects.filter(equipamento__id=id)
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    log=Log(transacao='eq',movimento='lt',usuario=usuario,equipamento=equipamento,alteracao=f'{usuario} listou detalhe equipamento: {equipamento}')
    log.save()
    return render(request, "exibirDetalheEquipamento.html", {'equipamento':equipamento, 'materiais':materiais, 'media':arquivos})

def editarEquipamento(request):
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Edição Equipamentos")
    if request.method=="GET":
        equipamento=request.GET.get("equipamento")
        dados=Equipamento.objects.get(id=equipamento)
        dados_paraformulario=dados.dados_para_form()
        form=equipamentoEditarForm(initial=dados_paraformulario) 
        log=Log(transacao='eq',movimento='lt',usuario=usuario,equipamento=dados,alteracao=f'{usuario} listou detalhe equipamento: {equipamento}')
        log.save()
        return render(request, "editarEquipamento.html", {'form':form})
    else:
        details = equipamentoEditarForm(request.POST)
        if details.is_valid():
            e=Equipamento.objects.get(id=details.cleaned_data['id'])
            log=Log(transacao='eq',movimento='ed',usuario=usuario,equipamento=e,alteracao=f'{usuario} editou equipamento{e}')
            log.save()
            if not(e.nome_equipamento==details.cleaned_data['nome_equipamento']):
                log=Log(transacao='eq',movimento='ed',usuario=usuario,equipamento=e,
                    alteracao=f"{usuario} editou nome do equipamento: {e.nome_equipamento} para {details.cleaned_data['nome_equipamento']}")
                log.save()
                e.nome_equipamento=details.cleaned_data['nome_equipamento']
                print(e.nome_equipamento)
            if not (e.modelo==details.cleaned_data['modelo']):
                log=Log(transacao='eq',movimento='ed',usuario=usuario,equipamento=e,
                    alteracao=f"{usuario} editou modelo do equipamento: {e.modelo} para {details.cleaned_data['modelo']}")
                log.save()
                e.modelo=details.cleaned_data['modelo']
            if not (e.fabricante==details.cleaned_data['fabricante']):
                log=Log(transacao='eq',movimento='ed',usuario=usuario,equipamento=e,
                    alteracao=f"{usuario} editou Fabricante do equipamento: {e.fabricante} para {details.cleaned_data['fabricante']}")
                log.save()
                e.fabricante=details.cleaned_data['fabricante']
            e.local=details.cleaned_data['local']
            e.tipo_equipamento=details.cleaned_data['tipo_equipamento']
            e.data_compra=details.cleaned_data['data_compra']
            e.data_ultima_calibracao=details.cleaned_data['data_ultima_calibracao']
            e.data_cadastro=details.cleaned_data['data_cadastro']
            e.patrimonio=details.cleaned_data['patrimonio']
            e.codigo=details.cleaned_data['codigo']
            e.save()
            usuario=Usuario.objects.get(id=request.session.get('usuario'))
            
            lista_materiais=Material_consumo.objects.filter(equipamento__id=details.cleaned_data['id'])
            for material in details.cleaned_data['material_consumo']:
                if material not in lista_materiais:
                    log=Log(transacao='mc',movimento='cd',usuario=usuario,equipmento=e,alteracao=f'{usuario} cadastrou {material} no {e}')
                    log.save()
                    e.material_consumo.add(material)
            for material in lista_materiais:
                if material not in details.cleaned_data['material_consumo']:
                    e.material_consumo.remove(material)
                    log=Log(transacao='mc',movimento='dl',usuario=usuario,equipmento=e,alteracao=f'{usuario} excluiu {material} do {e}')
                    log.save()
            
    equipamentos=Equipamento.objects.all()
    return render(request, "exibirEquipamentos.html", {'equipamentos':equipamentos})

def cadastrarEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Cadastro Equipamentos")
    if request.method=="GET":
        form=equipamentoCadastrarForm(initial={'usuario':request.session.get('usuario')})      

        return render(request, "cadastrarEquipamento.html", {'form':form,'status':0})
    else:
        details = equipamentoCadastrarForm(request.POST)

        if details.is_valid():
            nome_equipamento=details.cleaned_data['nome_equipamento']
            modelo=details.cleaned_data['modelo']
            fabricante=details.cleaned_data['fabricante']
            local=details.cleaned_data['local']
            tipo_equipamento=details.cleaned_data['tipo_equipamento']
            data_compra=details.cleaned_data['data_compra']
            data_ultima_calibracao=details.cleaned_data['data_ultima_calibracao']
            data_cadastro=details.cleaned_data['data_cadastro']
            patrimonio=details.cleaned_data['patrimonio']
            material_consumo=details.cleaned_data['material_consumo']
            usuario=details.cleaned_data['usuario']
            codigo=details.cleaned_data['codigo']
            custo_aquisição=details.cleaned_data['custo_aquisição']
            responsavel=details.cleaned_data['responsavel']
            potencia_eletrica=details.cleaned_data['potencia_eletrica']
            nacionalidade=details.cleaned_data['nacionalidade']
            data_ultima_atualizacao=details.cleaned_data['data_ultima_atualizacao']
            tensao_eletrica=details.cleaned_data['tensao_eletrica']
            projeto_compra=details.cleaned_data['projeto_compra']
            especificacao=details.cleaned_data['especificacao']
            outros_dados=details.cleaned_data['outros_dados']
            
            e= Equipamento(nome_equipamento=nome_equipamento,modelo=modelo,fabricante=fabricante,local=local,tipo_equipamento=tipo_equipamento,
                            data_cadastro=data_cadastro,data_compra=data_compra,data_ultima_calibracao=data_ultima_calibracao,patrimonio=patrimonio,
                            usuario=Usuario.objects.get(id=usuario),codigo=codigo,responsavel=responsavel,potencia_eletrica=potencia_eletrica,
                            nacionalidade=nacionalidade,data_ultima_atualizacao=data_ultima_atualizacao,tensao_eletrica=tensao_eletrica,
                            projeto_compra=projeto_compra,especificacao=especificacao,outros_dados=outros_dados,custo_aquisição=custo_aquisição)
            e.save()
            usuario=Usuario.objects.get(id=request.session.get('usuario'))
            log=Log(transacao='eq',movimento='cd',usuario=usuario,equipmento=e,alteracao=f'{usuario} cadastrou equipamento{e}')
            log.save()

            for material in material_consumo:
                e.material_consumo.add(material)
                log=Log(transacao='mc',movimento='cd',usuario=usuario,equipmento=e,alteracao=f'{usuario} cadastrou {material} no {e}')
                log.save()
            
            form=equipamentoCadastrarForm(initial={'usuario':request.session.get('usuario')}) 
            return render(request, "cadastrarEquipamento.html", {'form':form,'status':1})
        else:
            return render(request, "cadastrarEquipamento.html", {'form':details}) 

def listarFornecedores(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Lista Fornecedores")
    fornecedores=Fabricante.objects.all()
    return render(request, "listarFornecedores.html", {'fornecedores':fornecedores})

def exibirDetalheFornecedor(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Detalhe Fornecedores")
    id=str(request.GET.get('id'))
    fornecedor=Fabricante.objects.get(id=id)
    if fornecedor.endereco_fabricante==None: 
        fornecedor.endereco_fabricante=""
    if fornecedor.nome_contato_fabricante==None or fornecedor.nome_contato_fabricante=='None': 
        fornecedor.nome_contato_fabricante=""
    if fornecedor.telefone_contato==None : 
        fornecedor.telefone_contato=""
    if fornecedor.email_contato_fabricante==None : 
        fornecedor.email_contato_fabricante=""
    if fornecedor.site_Fabricante==None: 
        fornecedor.site_Fabricante=""
    if fornecedor.dados_adicionais==None : 
        fornecedor.dados_adicionais=""
    return render(request, "exibirDetalhefornecedor.html", {'fornecedor':fornecedor})

def cadastrarFornecedor(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Cadastro Fornecedores")
    status=str(request.GET.get('status'))
    if request.method=="GET":
        return render(request, "cadastrarFornecedor.html")
    else:
        # captura dados
        post_nome_fabricante=request.POST.get('nome_fabricante')
        post_endereco_fabricante=request.POST.get('endereco_fabricante')
        post_nome_contato_fabricante=request.POST.get('nome_contato_fabricante')
        post_telefone_contato=request.POST.get('telefone_contato')
        post_email_contato_fabricante=request.POST.get('email_contato_fabricante')
        post_site_Fabricante=request.POST.get('site_Fabricante')
        post_dados_adicionais=request.POST.get('dados_adicionais')
        #verifica campo vazio e coloca None
        if post_endereco_fabricante=="" : 
            post_endereco_fabricante=None
        if post_nome_contato_fabricante=="" : 
            post_nome_contato_fabricante=None
        if post_telefone_contato=="" : 
            post_telefone_contato=None
        if post_email_contato_fabricante=="" : 
            post_email_contato_fabricante=None
        if post_site_Fabricante=="" : 
            post_site_Fabricante=None
        if post_dados_adicionais=="" : 
            post_dados_adicionais=None
        #busca por dados repetidos no banco de dados
        nome=Fabricante.objects.filter(nome_fabricante=post_nome_fabricante).first()
        site=Fabricante.objects.filter(site_Fabricante=post_site_Fabricante).first()
        email=Fabricante.objects.filter(email_contato_fabricante=post_email_contato_fabricante).first()
        # verifica se forncedor ja existe
        if nome and site and email: 
            return render(request, "cadastrarFornecedor.html", {'status':1}) # fornecedor ja cadastrado
        # verifica se estão preenchidos campos obrigatórios
        if not post_nome_fabricante:
            return render(request, "cadastrarFornecedor.html", {'status':2}) # campos obrigatórios não preenchidos
        # verfica digitação do email e do telefone
        regex_email= '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        #if post_email_contato_fabricante:
        #    if not (re.search(regex_email, post_email_contato_fabricante)):
        #        return render(request, "cadastrarFornecedor.html", {'status':3}) # email com digitação incorreta
        fabricante= Fabricante(nome_fabricante=post_nome_fabricante,
                                endereco_fabricante=post_endereco_fabricante,
                                nome_contato_fabricante=post_nome_contato_fabricante,
                                telefone_contato=post_telefone_contato,
                                email_contato_fabricante=post_email_contato_fabricante,
                                site_Fabricante=post_site_Fabricante,
                                dados_adicionais=post_dados_adicionais)
        fabricante.save()
        return render(request, "cadastrarFornecedor.html", {'status':0})

def editarFornecedor(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Edição Fornecedores")
    id=request.GET.get('id')

    if id:
        if request.method=="GET":
            fornecedor=Fabricante.objects.get(id=id)
            return render(request, "editarFornecedor.html",{"fornecedor":fornecedor})
    if request.method=="POST":
        post_id=request.POST.get('id')
        post_nome_fabricante=request.POST.get('nome_fabricante')
        post_endereco_fabricante=request.POST.get('endereco_fabricante')
        post_nome_contato_fabricante=request.POST.get('nome_contato_fabricante')
        post_telefone_contato=request.POST.get('Telefone_contato_fabricante')
        post_email_contato_fabricante=request.POST.get('email_contato_fabricante')
        post_site_Fabricante=request.POST.get('site_Fabricante')
        post_dados_adicionais=request.POST.get('dados_adicionais')
        #verifica campo vazio e coloca None
        if post_endereco_fabricante=="" or post_endereco_fabricante=='None': 
            post_endereco_fabricante=None
        if post_nome_contato_fabricante=="" or post_nome_contato_fabricante=="None" : 
            post_telefone_contato=None
        if post_telefone_contato=="" or post_telefone_contato=="None" : 
            post_telefone_contato=None
        if post_email_contato_fabricante=="" or post_email_contato_fabricante=="None" : 
            post_email_contato_fabricante=None
        if post_site_Fabricante==""  or post_site_Fabricante=="None ": 
            post_site_Fabricante=None
        if post_dados_adicionais=="" or post_dados_adicionais=="None" : 
            post_dados_adicionais=None
        fornecedor=Fabricante.objects.get(id=post_id)
        #busca por dados repetidos no banco de dados
        nome=Fabricante.objects.filter(nome_fabricante=post_nome_fabricante).first()
        site=Fabricante.objects.filter(site_Fabricante=post_site_Fabricante).first()
        email=Fabricante.objects.filter(email_contato_fabricante=post_email_contato_fabricante).first()
        #print(post_nome_fabricante)
        # verifica se forncedor ja existe
        if (nome and nome.id!=fornecedor.id) and site and email: 
            return render(request, "editarFornecedor.html", {'fornecedor':fornecedor,'status':1}) # fornecedor ja cadastrado
        # verifica se estão preenchidos campos obrigatórios
        if not post_nome_fabricante:
            return render(request, "editarFornecedor.html", {'fornecedor':fornecedor,'status':2}) # campos obrigatórios não preenchidos
        # verfica digitação do email e do telefone
        regex_email= '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        #if post_email_contato_fabricante:
            #if not (re.search(regex_email, post_email_contato_fabricante)):
                #return render(request, "editarFornecedor.html", {'fornecedor':fornecedor,'status':3}) # email com digitação incorreta
        
        
        fornecedor.nome_fabricante=post_nome_fabricante
        fornecedor.endereco_fabricante=post_endereco_fabricante
        fornecedor.nome_contato_fabricante=post_nome_contato_fabricante
        fornecedor.telefone_contato=post_telefone_contato
        fornecedor.email_contato_fabricante=post_email_contato_fabricante
        fornecedor.site_Fabricante=post_site_Fabricante
        fornecedor.dados_adicionais=post_dados_adicionais
        fornecedor.save()
        return redirect('/equipamentos/listarFornecedores/?status=10')
        
    
    return redirect('/equipamentos/listarFornecedores/')

def cadastrarLocal(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou cadastro local")
    if request.method=="GET":
        form=localFormCadastro
        return render(request, "cadastrarLocal.html", {'form':form,'status':0})
    else:
        details = localFormCadastro(request.POST)
        if details.is_valid():
            print('valido')
            details.save()
            form=localFormCadastro
                        
            return render(request, "cadastrarLocal.html", {'form':form,'status':1})
        else:
            print('invalido')
            return render(request, "cadastrarLocal.html", {'form':details}) 

def listarLocais(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Listar local")
    if request.method=="GET":
        form = Local_instalacao.objects.all()
        return render(request, "listarLocais.html", {'form':form,'status':0}) 
def editarLocal(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Editar local")
    if request.method=="GET":
        dados = Local_instalacao.objects.get(id=request.GET.get("id")).dados_para_form()
        form=localFormEditar(initial=dados) 
        return render(request, "editarLocal.html", {'form':form,'id':request.GET.get("id"),'status':0}) 
    else:
        form = Local_instalacao.objects.all()        
        details = localFormEditar(request.POST)
        if details.is_valid():

            e=Local_instalacao.objects.get(id=details.cleaned_data['id'])
            e.predio=details.cleaned_data['predio']
            e.piso=details.cleaned_data['piso']
            e.sala=details.cleaned_data['sala']
            e.armario=details.cleaned_data['armario']
            e.prateleira=details.cleaned_data['prateleira']
            e.apelido_local=details.cleaned_data['apelido_local']
            e.save()
            
            return render(request, "listarLocais.html", {'form':form,'status':1}) 
        else:
            return render(request, "listarLocais.html", {'form':form,'status':2})

def cadastrarTipo(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou cadastro Tipo Equipamento")
    if request.method=="GET":
        form=cadastraTipo_equipamento
        return render(request, "cadastrarTipo.html", {'form':form,'status':0})
    else:
        details = cadastraTipo_equipamento(request.POST)
        if details.is_valid():
            print('valido')
            
            tipo=Tipo_equipamento(nome_tipo=details.cleaned_data['nome'],sigla=details.cleaned_data['sigla'],descricao_tipo=details.cleaned_data['descricao'])
            tipo.save()
            form=cadastraTipo_equipamento
                        
            return render(request, "cadastrarTipo.html", {'form':form,'status':1})
        else:
            print('invalido')
            return render(request, "cadastrarTipo.html", {'form':details}) 
def editarTipo(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou cadastro Tipo Equipamento")
    if request.method=="GET":
        dados = Tipo_equipamento.objects.get(id=request.GET.get("id")).dados_para_form()
        print(dados)
        form=TipoEquipamentoForm(initial=dados)
        return render(request, "editarTipo.html",{'form':form,'id':request.GET.get("id"),'status':0}) 
    else:
        details = TipoEquipamentoForm(request.POST)
        if details.is_valid():
            print('valido')
            tipo=Tipo_equipamento.objects.get(id=details.cleaned_data['id'] )
            tipo.nome_tipo=details.cleaned_data['nome_tipo']
            tipo.descricao_tipo=details.cleaned_data['descricao']
            tipo.save()
            form=Tipo_equipamento.objects.all()
            return render(request, "listarTipo.html", {'form':form,'status':1})
        else:
            print('invalido')
            return render(request, "editarTipo.html", {'form':details}) 
def listarTipo(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou cadastro Tipo Equipamento")

    form=Tipo_equipamento.objects.all()
    return render(request, "listarTipo.html", {'form':form,'status':0})

def importaDados(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    if request.GET.get('campo')=='local':
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
        return HttpResponse(conteudo)
    elif request.GET.get('campo')=='tipo':
        caminho=os.path.join(BASE_DIR,"banco Migrado",'tipo.csv')
        arquivo=open(caminho,'r', encoding='utf-8')
        dados=arquivo.readline()
        dados=arquivo.readline()
        conteudo=[]
        while(dados):
            dado=dados.split(";") 
            print(dado[0], len(dados[0]))
            if dado[0]!="" and len(dado[0])>=3:
                
                conteudo.append(dado)
                tipos=Tipo_equipamento.objects.all()
                siglas=[]
                for tipo in tipos:
                    siglas.append(tipo.sigla)
                sigla=dado[0][:3].upper()

                i=3
                j=2
                while(sigla in siglas  and i<len(dado[0])):
                    if dado[0][i:6-j].upper()!=" ":
                        sigla=dado[0][0:j].upper()+dado[0][i:6-j].upper()
                    else:
                        sigla=dado[0][0:j].upper()+dado[0][i+1:7-j].upper()
                    i+=1
                    if i>len(dado[0]):
                        sigla=dado[0][0:j].upper()+'X'*(3-j)
                        j-=1
                print(sigla)
                tipo=Tipo_equipamento(nome_tipo=dado[0], sigla=sigla)
                tipo.save()
            dados=arquivo.readline()
        arquivo.close()
        return HttpResponse(conteudo)
    elif request.GET.get('campo')=='fabricante':
        caminho=os.path.join(BASE_DIR,"banco Migrado",'fabricante.csv')
        arquivo=open(caminho,'r', encoding='utf-8')
        dados=arquivo.readline()
        dados=arquivo.readline()
        conteudo=[]
        while(dados):
            dado=dados.split(";") 
            if dado[0]!="" and len(dado[0])>=3:
                conteudo.append(dado)   
                fabricante=Fabricante(nome_fabricante=dado[0])
                fabricante.save()
            dados=arquivo.readline()
        arquivo.close()
        return HttpResponse(conteudo)
    elif request.GET.get('campo')=='equipamento':
        caminho=os.path.join(BASE_DIR,"banco Migrado",'equipamentos.csv')
        arquivo=open(caminho,'r', encoding='utf-8')
        conteudo=""
        dados=arquivo.readline()
        dados=dados.split(";")
        conteudo+="<h1>"
        for i,dado in enumerate(dados):
            conteudo+=str(i)+"-"+str(dado)+'  '
        conteudo+="</h1><br>"
        dados=arquivo.readline()
        cont=0
        while(dados):
            dado=dados.split(";") 
            if dado[0]!="" and len(dado[0])>=3:
                print(cont)
                cont+=1
                conteudo+=str(dados)+"<br>"
                fabricante=Fabricante.objects.filter(nome_fabricante__contains=dado[7])
                if len(fabricante)==0:
                    fabricante=[None]
                local=Local_instalacao.objects.filter(laboratorio=dado[0],predio=dado[1])
                if len(local)==0:
                    local=[None]
                tipo=Tipo_equipamento.objects.filter(nome_tipo=dado[6])
                if len(tipo)==0:
                    tipo=Tipo_equipamento.objects.filter(nome_tipo='outros')
                usuario=Usuario.objects.filter(nome="System")
                eqptos=Equipamento.objects.filter(tipo_equipamento=tipo[0])
                numero=len(eqptos)+1
                codigo=f'{tipo[0].sigla.upper()}{numero:03d}'
                utc=pytz.UTC
                hoje=utc.localize( datetime.datetime.now())
                if len(dado[15])>2:
                    tensao=dado[15]
                if len(dado[15])>2:
                    tensao+="/"+dado[16]
                tensao+="V"
                if len(dados[17])>2:
                    tensao+=f"-{dados[17]} - {dado[18]}"
                try:
                    ano=int(dado[25])
                except:
                    ano=1900
                data_compra=utc.localize(datetime.datetime(ano,1,1))
                try:
                    valor=float(dado[9])
                except:
                    valor=0.01


                equipamento=Equipamento(nome_equipamento=dado[4],fabricante=fabricante[0],local=local[0],modelo=dado[19],
                        tipo_equipamento=tipo[0],data_compra=data_compra,usuario=usuario[0],patrimonio=dado[28],
                        codigo=codigo, custo_aquisição=valor,custo_aquisição_currency="BRL",responsavel=dado[12].capitalize(),
                        potencia_eletrica=dado[13]+dado[14],nacionalidade=dado[24],data_ultima_atualizacao= hoje,
                        tensao_eletrica=tensao,projeto_compra=dado[26],especificacao=dado[20]+" "+dado[22],
                        outros_dados=dado[29])
                equipamento.save()
            dados=arquivo.readline()
        arquivo.close()
        return HttpResponse(conteudo)
    return HttpResponse("Erro")
