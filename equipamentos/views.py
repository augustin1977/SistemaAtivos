# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.staticfiles.views import serve
from django.http import HttpResponse
from .models import Usuario,Tipo,Equipamento,Material_consumo,Media,Fabricante
from django.shortcuts import redirect 
from cadastro_equipamentos import settings
from django.http import HttpResponse, Http404
from os import path
import urllib.request
from cadastro_equipamentos.settings import BASE_DIR,MEDIA_ROOT,TIME_ZONE
import os,csv
from log.models import Log
from .forms import *
import equipamentos.funcoesAuxiliares as funcoesAuxiliares
from django.db.models import Q
def home(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    # cria a view do login do usuário
    status=str(request.GET.get('status'))
    return render(request, "home.html", {'status':status})
def menuEquipoamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    # cria a view do login do usuário
    status=str(request.GET.get('status'))
    return render(request, "equipamentos.html", {'status':status})

def lista_equipamentos(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    usu=Usuario.objects.get(id=request.session.get('usuario'))
    print(f"{usu.nome} acessou Lista Equipamentos")
    equipamentos=Equipamento.objects.filter(ativo=True)
    return render(request, "exibirEquipamentos.html", {'equipamentos':equipamentos})

def exibirDetalheEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Detalhe Equipamentos")
    id=str(request.GET.get('id'))
    equipamento=Equipamento.objects.get(id=id,ativo=True)
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
    if request.method=="GET":
        equipamento=request.GET.get("equipamento")
        dados=Equipamento.objects.get(id=equipamento,ativo=True)
        dados_paraformulario=dados.dados_para_form()
        form=equipamentoEditarForm(initial=dados_paraformulario) 
        return render(request, "editarEquipamento.html", {'form':form})
    else:
        details = equipamentoEditarForm(request.POST)
        if details.is_valid():     
            e=Equipamento.objects.get(id=details.cleaned_data['id'],ativo=True)
            listaCampos=['nome_equipamento','modelo','fabricante','local','tipo_equipamento','data_compra',
                         'data_ultima_calibracao','data_cadastro','patrimonio','codigo',
                         'custo_aquisição','responsavel','potencia_eletrica','nacionalidade','data_ultima_atualizacao',
                         'tensao_eletrica','projeto_compra','especificacao','outros_dados']
            alteracao=False
            for campo in listaCampos:
                alterado=Log.foiAlterado(transacao='eq',objeto=e,atributo=campo,equipamento=e,
                                 valor=details.cleaned_data[campo],usuario=usuario) 
                if alterado:
                    setattr(e,campo,details.cleaned_data[campo])
                alteracao|=alterado
            if alteracao:
                e.save()
            
            lista_materiais=Material_consumo.objects.filter(equipamento__id=details.cleaned_data['id'])
            for material in details.cleaned_data['material_consumo']:
                if material not in lista_materiais:
                    log=Log(transacao='mc',usuario=usuario,equipamento=e,alteracao=f'O usuario {usuario} cadastrou o material {material} no equipamento {e}')
                    log.save()
                    e.material_consumo.add(material)
            for material in lista_materiais:
                if material not in details.cleaned_data['material_consumo']:
                    e.material_consumo.remove(material)
                    log=Log(transacao='mc',movimento='dl',usuario=usuario,equipmento=e,alteracao=f'o usuario {usuario} excluiu o material {material} do equipamento {e}')
                    log.save()
            
    equipamentos=Equipamento.objects.filter(ativo=True)
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
                            projeto_compra=projeto_compra,especificacao=especificacao,outros_dados=outros_dados,custo_aquisição=custo_aquisição,ativo=True)
            e.save()
            usuario=Usuario.objects.get(id=request.session.get('usuario'))
            Log.cadastramento(objeto=e,transacao='eq',usuario=usuario,equipamento=e)
            

            for material in material_consumo:
                e.material_consumo.add(material)
                log=Log(transacao='mc',movimento='cd',usuario=usuario,equipmento=e,alteracao=f'o usuario {usuario} cadastrou o {material} no equipamento {e} id={e.id}')
                log.save()
            
            form=equipamentoCadastrarForm(initial={'usuario':request.session.get('usuario')}) 
            return render(request, "cadastrarEquipamento.html", {'form':form,'status':1})
        else:
            return render(request, "cadastrarEquipamento.html", {'form':details}) 
        
def excluirEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    id=str(request.GET.get('id'))
    equipamento=Equipamento.objects.get(id=id,ativo=True)
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    if request.GET.get('excluir')=='2':
        equipamento.ativo=False
        equipamento.save()
        Log.exclusao(objeto=equipamento,transacao='eq',usuario=usuario,equipamento=equipamento)
        return redirect('/equipamentos/listarEquipamentos')
    
    materiais=Material_consumo.objects.filter(equipamento__id=id)
    arquivos= Media.objects.filter(equipamento__id=id)
    print('excluir',request.GET.get('excluir'))
    return render(request, "exibirDetalheEquipamento.html", {'equipamento':equipamento, 
                                                             'materiais':materiais, 
                                                             'media':arquivos, 
                                                             'confirmarexluir':request.GET.get('excluir')})

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
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
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
        Log.cadastramento(usuario=usuario,transacao='li',objeto=fabricante)
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
        usuario=Usuario.objects.get(id=request.session.get('usuario'))
        if Log.foiAlterado(objeto=fornecedor,atributo='nome_fabricante',valor=post_nome_fabricante,usuario=usuario,transacao='fn'):
            fornecedor.nome_fabricante=post_nome_fabricante
        if Log.foiAlterado(objeto=fornecedor,atributo='endereco_fabricante',valor=post_endereco_fabricante,usuario=usuario,transacao='fn'):
            fornecedor.endereco_fabricante=post_endereco_fabricante
        if Log.foiAlterado(objeto=fornecedor,atributo='nome_contato_fabricante',valor=post_nome_contato_fabricante,usuario=usuario,transacao='fn'):
            fornecedor.nome_contato_fabricante=post_nome_contato_fabricante
        if Log.foiAlterado(objeto=fornecedor,atributo='telefone_contato',valor=post_telefone_contato,usuario=usuario,transacao='fn'):
            fornecedor.telefone_contato=post_telefone_contato
        if Log.foiAlterado(objeto=fornecedor,atributo='email_contato_fabricante',valor=post_email_contato_fabricante,usuario=usuario,transacao='fn'):
            fornecedor.email_contato_fabricante=post_email_contato_fabricante
        if Log.foiAlterado(objeto=fornecedor,atributo='site_Fabricante',valor=post_site_Fabricante,usuario=usuario,transacao='fn'):
            fornecedor.site_Fabricante=post_site_Fabricante
        if Log.foiAlterado(objeto=fornecedor,atributo='dados_adicionais',valor=post_dados_adicionais,usuario=usuario,transacao='fn'):
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
            print(details)
            details.save()
            form=localFormCadastro
            usuario=Usuario.objects.get(id=request.session.get('usuario'))
           
            local=Local_instalacao.objects.get(laboratorio=details.cleaned_data['laboratorio'],sala=details.cleaned_data['sala'],
                                            predio=details.cleaned_data['predio'],piso=details.cleaned_data['piso'],apelido_local=details.cleaned_data['apelido_local'],
                                            armario=details.cleaned_data['armario'],prateleira=details.cleaned_data['prateleira'] )
            Log.cadastramento(usuario=usuario,transacao='li',objeto=local)            
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
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{usuario.nome} acessou Editar local")
    if request.method=="GET":
        dados = Local_instalacao.objects.get(id=request.GET.get("id")).dados_para_form()
        form=localFormEditar(initial=dados) 
        return render(request, "editarLocal.html", {'form':form,'id':request.GET.get("id"),'status':0}) 
    else:
        form = Local_instalacao.objects.all()        
        details = localFormEditar(request.POST)
        if details.is_valid():
            e=Local_instalacao.objects.get(id=details.cleaned_data['id'])
            listaCampos=['laboratorio','predio','piso','sala','armario','prateleira','apelido_local']
            alteracao=False
            for campo in listaCampos:
                alterado=Log.foiAlterado(transacao='li',objeto=e,atributo=campo,valor=details.cleaned_data[campo],usuario=usuario) 
                if alterado:
                    setattr(e,campo,details.cleaned_data[campo])
                alteracao|=alterado
            if alteracao:
                e.save()            
            return render(request, "listarLocais.html", {'form':form,'status':1}) 
        else:
            return render(request, "listarLocais.html", {'form':form,'status':2})

def cadastrarTipo(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    usuario =Usuario.objects.get(id=request.session.get('usuario'))
    print(f"{usuario.nome} acessou cadastro Tipo Equipamento")
    
    if request.method=="GET":
        form=cadastraTipo_equipamento
        return render(request, "cadastrarTipo.html", {'form':form,'status':0})
    else:
        details = cadastraTipo_equipamento(request.POST)
        if details.is_valid():
            print('valido')
            
            tipo=Tipo_equipamento(nome_tipo=details.cleaned_data['nome'],sigla=details.cleaned_data['sigla'],descricao_tipo=details.cleaned_data['descricao'])
            tipo.save()
            Log.cadastramento(usuario=usuario,transacao='te',objeto=tipo)
            form=cadastraTipo_equipamento
                        
            return render(request, "cadastrarTipo.html", {'form':form,'status':1})
        else:
            print('invalido')
            return render(request, "cadastrarTipo.html", {'form':details}) 

def editarTipo(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    usuario =Usuario.objects.get(id=request.session.get('usuario'))
    print(f"{usuario.nome} acessou cadastro Tipo Equipamento")
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
            listaCampos=['nome_tipo','descricao_tipo']
            alteracao=False
            for campo in listaCampos:
                alterado=Log.foiAlterado(transacao='te',objeto=tipo,atributo=campo,valor=details.cleaned_data[campo],usuario=usuario) 
                if alterado:
                    setattr(tipo,campo,details.cleaned_data[campo])
                alteracao|=alterado
            if alteracao:
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

def baixarRelatorioEquipamentos(request):

    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio.csv"'

    # Crie um objeto CSV Writer
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=';')

    # Escreva o cabeçalho do arquivo CSV
    writer.writerow(['Nome_equipamento', 'modelo', 'fabricante','local','tipo_equipamento',
        'data_compra','data_ultima_calibracao','usuario_cadastro','data_cadastro',
        'patrimonio','codigo','custo_aquisição','moeda','projeto_compra','responsavel','potencia_eletrica',
        'tensao_eletrica','nacionalidade','data_ultima_atualizacao','especificacao','dados_adicionais','ativo'])

    # Execute a consulta no banco de dados e adicione os resultados ao arquivo CSV
    for obj in Equipamento.objects.all().order_by('-nome_equipamento'):
        writer.writerow([obj.nome_equipamento, obj.modelo, obj.fabricante,obj.local,obj.tipo_equipamento,
            obj.data_compra,obj.data_ultima_calibracao,obj.usuario,obj.data_cadastro,
            obj.patrimonio,obj.codigo,obj.custo_aquisição,obj.custo_aquisição_currency,obj.projeto_compra,
            obj.responsavel,obj.potencia_eletrica,obj.tensao_eletrica,obj.nacionalidade,
            obj.data_ultima_atualizacao,obj.especificacao,obj.outros_dados,obj.ativo])

    return response

def cadastrarMaterial(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    usu=Usuario.objects.get(id=request.session.get('usuario'))
    print(f"{usu.nome} acessou cadastro Cadastro Material")
    
    if request.method=="GET":
        form=materialCadastraForm
        return render(request, "cadastrarMaterial.html", {'form':form,'status':0})
    else:
        details = materialCadastraForm(request.POST)
        if details.is_valid():
            details.save()
            material=Material_consumo.objects.get(nome_material=details.cleaned_data['nome_material'],
                                                  fornecedor=details.cleaned_data['fornecedor'],
                                                  especificacao_material=details.cleaned_data['especificacao_material'],
                                                  unidade_material=details.cleaned_data['unidade_material'])
            Log.cadastramento(usuario=usu,transacao='mc',objeto=material)
            
            form=materialCadastraForm
                        
            return render(request, "cadastrarMaterial.html", {'form':form,'status':1})
        else:
            print('invalido')
            return render(request, "cadastrarMaterial.html", {'form':details,'status':2}) 

def editarMaterial(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Editar Material")
    if request.method=="GET":
        dados = Material_consumo.objects.get(id=request.GET.get("id")).dados_para_form()
        form=materialCadastraForm(initial=dados) 
        return render(request, "editarMAterial.html", {'form':form,'id':request.GET.get("id"),'status':0}) 
    else:
        form = Material_consumo.objects.all()        
        details = materialCadastraForm(request.POST)
        if details.is_valid():
            mat=Material_consumo.objects.get(id=details.cleaned_data['id'])
            usuario=Usuario.objects.get(id=request.session.get('usuario'))
            listaCampos=['nome_material','fornecedor','especificacao_material','unidade_material','unidade_material','simbolo_unidade_material']
            alteracao=False
            for campo in listaCampos:
                alterado=Log.foiAlterado(transacao='mc',objeto=mat,atributo=campo,valor=details.cleaned_data[campo],usuario=usuario) 
                if alterado:
                    setattr(mat,campo,details.cleaned_data[campo])
                alteracao|=alterado
            if alteracao:
                mat.save() 
            return render(request, "listarMateriais.html", {'form':form,'status':1}) 
        else:
            return render(request, "listarMateriais.html", {'form':form,'status':2})

def listarMaterial(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Listar materiais")
    if request.method=="GET":
        form = Material_consumo.objects.all()
        return render(request, "listarMateriais.html", {'form':form,'status':0})

def cadastrarArquivo(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    if request.method == 'POST':
        form = mediaForm(request.POST, request.FILES)
        if form.is_valid():
            media=Media(nome=form.cleaned_data['nome'],
                        documentos=form.cleaned_data['documentos'],
                        equipamento=form.cleaned_data['equipamento'])
            usuario=Usuario.objects.get(id=request.session.get('usuario'))
            media.save()
            Log.cadastramento(usuario=usuario,transacao='me',objeto=media)
            return redirect('cadastrarArquivo')
        else:
            print("Falhou")
    else:
        form = mediaForm()
    return render(request, 'cadastrarArquivo.html', {'form': form})

def excluiArquivo(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    if request.method == 'GET':
       media=Media.objects.get(id=request.GET.get('id'))
       id_equipamento=media.equipamento.id
       fullpath = os.path.normpath(os.path.join(MEDIA_ROOT, str(media.documentos)))
       os.remove(fullpath)
       media.delete()
       return  redirect(f'/equipamentos/exibirDetalheEquipamento/?id={id_equipamento}')
    
    return HttpResponse("formulario de excluir arquivos")

def download_arquivo(request):
    nome_arquivo=request.POST.get('filename')
    #caminho=os.path.join(MEDIA_ROOT,nome_arquivo)
    fullpath = os.path.normpath(os.path.join(MEDIA_ROOT, nome_arquivo))
    print(fullpath, MEDIA_ROOT)
    if not fullpath.startswith(MEDIA_ROOT[:-1]):
        raise PermissionError
    with open(fullpath, 'rb') as arquivo:
        figuras=["jpg","bmp",'gif','svg','png']
        if nome_arquivo[-3:].lower() in figuras:
            
            response = HttpResponse(arquivo.read(), content_type='image')
        else:
            response = HttpResponse(arquivo.read(), content_type='application/octet-stream')
        filename=nome_arquivo.split("/")
        response['Content-Disposition'] = f'attachment; filename="{filename[1]}"'
    return response   


def excluirTipo(request):
    
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=1')
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo1=Q(tipo="especialuser")
    tipo2=Q(tipo="superuser")
    tipo3=Q(tipo="admin")
    tipo=Tipo.objects.filter(tipo1 | tipo2| tipo3)
    if(usuario.tipo in tipo):
        if request.method=="GET":
            tipo_eq=request.GET.get("id")
            tipo_equipamento=Tipo_equipamento.objects.get(id=tipo_eq)
            equipamentos=Equipamento.objects.filter(tipo_equipamento=tipo_equipamento)
            return render (request,'excluirTipo.html',{'n':len(equipamentos),'equipamentos':equipamentos,'tipo':tipo_equipamento})
        elif request.method=="POST":
            tipo_eq=request.POST.get("id")
            tipo_equipamento=Tipo_equipamento.objects.get(id=tipo_eq)
            equipamentos=Equipamento.objects.filter(tipo_equipamento=tipo_equipamento)
            outros=Tipo_equipamento.objects.get(nome_tipo="Outros")
            for equipamento in equipamentos:
                print(equipamento)
                Log.foiAlterado(transacao='eq',objeto=equipamento,atributo="tipo_equipamento",equipamento=equipamento,
                                 valor=outros,usuario=usuario) 
                equipamento.tipo_equipamento=outros
                equipamento.save()
            Log.exclusao(usuario=usuario,transacao="te",objeto=tipo_equipamento)    
            tipo_equipamento.delete()
            
            return redirect('/equipamentos/listarTipo')
        
           

    return HttpResponse("funcionalidade não implementada")

def excluirLocal(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=1')
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo1=Q(tipo="especialuser")
    tipo2=Q(tipo="superuser")
    tipo3=Q(tipo="admin")
    tipo=Tipo.objects.filter(tipo1 | tipo2| tipo3)
    if(usuario.tipo in tipo):
        if request.method=="GET":
            loc=request.GET.get("id")
            local=Local_instalacao.objects.get(id=loc)
            equipamentos=Equipamento.objects.filter(local=local)
            return render (request,'excluirLocal.html',{'n':len(equipamentos),'equipamentos':equipamentos,'local':local})
        elif request.method=="POST":
            loc=request.POST.get("id")
            local=Tipo_equipamento.objects.get(id=loc)
            Log.exclusao(usuario=usuario,transacao="le",objeto=local)    
            local.delete()
            return redirect('/equipamentos/listarLocais')
        
           

    return HttpResponse("funcionalidade não implementada")