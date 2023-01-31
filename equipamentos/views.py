from django.shortcuts import render
from django.contrib.staticfiles.views import serve
from django.http import HttpResponse
from .models import Usuario,Tipo,Equipamento,Material_consumo,Media,Fabricante
from django.shortcuts import redirect 
from hashlib import sha256
from cadastro_equipamentos import settings
from django.http import HttpResponse, Http404
from os import path
import mimetypes
from django.utils.encoding import smart_str
import re
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
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Lista Equipamentos")
    equipamentos=Equipamento.objects.all()
    return render(request, "exibirEquipamentos.html", {'equipamentos':equipamentos})

def exibirDetalheEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Detalhe Equipamentos")
    id=str(request.GET.get('id'))
    equipamento=Equipamento.objects.get(id=id)
    materiais=Material_consumo.objects.filter(equipamento__id=id)
    arquivos= Media.objects.filter(equipamento__id=id)
    return render(request, "exibirDetalheEquipamento.html", {'equipamento':equipamento, 'materiais':materiais, 'media':arquivos})

def editarEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Edição Equipamentos")
    if request.method=="GET":
        equipamento=request.GET.get("equipamento")
        dados=Equipamento.objects.get(id=equipamento)
        dados_paraformulario=dados.dados_para_form()
        form=equipamentoEditarForm(initial=dados_paraformulario) 
        
        return render(request, "editarEquipamento.html", {'form':form})
    else:
        details = equipamentoEditarForm(request.POST)
        if details.is_valid():
            e=Equipamento.objects.get(id=details.cleaned_data['id'])
            e.nome_equipamento=details.cleaned_data['nome_equipamento']
            e.modelo=details.cleaned_data['modelo']
            e.fabricante=details.cleaned_data['fabricante']
            e.local=details.cleaned_data['local']
            e.tipo_equipamento=details.cleaned_data['tipo_equipamento']
            e.data_compra=details.cleaned_data['data_compra']
            e.data_ultima_calibracao=details.cleaned_data['data_ultima_calibracao']
            e.data_cadastro=details.cleaned_data['data_cadastro']
            e.patrimonio=details.cleaned_data['patrimonio']

            e.codigo=details.cleaned_data['codigo']
            e.save()
            lista_materiais=Material_consumo.objects.filter(equipamento__id=details.cleaned_data['id'])
            for material in details.cleaned_data['material_consumo']:
                if material not in lista_materiais:
                    e.material_consumo.add(material)
            for material in lista_materiais:
                if material not in details.cleaned_data['material_consumo']:
                    e.material_consumo.remove(material)
            
    fornecedores=Fabricante.objects.all()
    return render(request, "listarFornecedores.html", {'fornecedores':fornecedores})

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
            e= Equipamento(nome_equipamento=nome_equipamento,modelo=modelo,fabricante=fabricante,local=local,tipo_equipamento=tipo_equipamento,
                            data_cadastro=data_cadastro,data_compra=data_compra,data_ultima_calibracao=data_ultima_calibracao,patrimonio=patrimonio,
                            usuario=Usuario.objects.get(id=usuario),codigo=codigo)
            e.save()

            for material in material_consumo:
                e.material_consumo.add(material)
            
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
        post_telefone_contato=request.POST.get('telefone_contato')
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


def download_view(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Download fotos")
    objeto=request.GET.get('filename')
    local=settings.MEDIA_ROOT[:-1]
    
    caminho=path.join(local,objeto)
    print(local," | ",objeto," | ",caminho)
    
    if not (path.exists(caminho)):
        raise Http404()

    mimetype, encoding = mimetypes.guess_type(caminho)
    
    if mimetype is None:
        mimetype = 'application/force-download'
      
    response = HttpResponse()
    response['Content-Type'] = mimetype
    response['Pragma'] = 'public'
    response['Expires'] = '100'
    response['Cache-Control'] = 'must-revalidate, post-check=0, pre-check=0'
    response['Content-Disposition'] = f'attachment; filename={caminho}'
    #response['Content-Transfer-Encoding'] = 'binary'
    #response['Content-Length'] = str(path.getsize(caminho))
    return response