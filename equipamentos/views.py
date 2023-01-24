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
    equipamentos=Equipamento.objects.all()
    return render(request, "exibirEquipamentos.html", {'equipamentos':equipamentos})

def exibirDetalheEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    id=str(request.GET.get('id'))
    equipamento=Equipamento.objects.get(id=id)
    materiais=Material_consumo.objects.filter(equipamento__id=id)
    arquivos= Media.objects.filter(equipamento__id=id)
    return render(request, "exibirDetalheEquipamento.html", {'equipamento':equipamento, 'materiais':materiais, 'media':arquivos})



def download_view(request):
    objeto=request.GET.get('filename')
    local=settings.MEDIA_ROOT[:-1]
    caminho=path.join(local,objeto)
    print(local," | ",objeto," | ",caminho)
    
    if not (path.exists(caminho)):
        raise Http404()

    mimetype, encoding = mimetypes.guess_type(caminho)
    
    if mimetype is None:
        mimetype = 'application/force-download'

    file = caminho.split("/")[-1]
    
    response = HttpResponse()
    response['Content-Type'] = mimetype
    response['Pragma'] = 'public'
    response['Expires'] = '0'
    response['Cache-Control'] = 'must-revalidate, post-check=0, pre-check=0'
    response['Content-Disposition'] = 'attachment; filename=%s' % objeto
    response['Content-Transfer-Encoding'] = 'binary'
    response['Content-Length'] = str(path.getsize(caminho))
    return response

def editarEquipamento(request):
    pass

def cadastrarEquipamento(request):
    
    if request.method=="GET":
        form=equipamentoCadastrarForm

        return render(request, "cadastrarEquipamento.html", {'form':form,'status':0})
    else:
        details = equipamentoCadastrarForm(request.POST)
        if details.is_valid():
            details.save()
            form=localFormCadastro
            return render(request, "cadastrarEquipamento.html", {'form':form,'status':1})
        else:
            return render(request, "cadastrarEquipamento.html", {'form':details}) 

def listarFornecedores(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    fornecedores=Fabricante.objects.all()
    return render(request, "listarFornecedores.html", {'fornecedores':fornecedores})

def exibirDetalheFornecedor(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
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
    return render(request, "exibirDetalheFornecedor.html", {'fornecedor':fornecedor})

def cadastrarFornecedor(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
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
        if post_email_contato_fabricante:
            if not (re.search(regex_email, post_email_contato_fabricante)):
                return render(request, "cadastrarFornecedor.html", {'status':3}) # email com digitação incorreta
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
    
    if request.method=="GET":
        form=localFormCadastro
        #print(form)
        #form.predio.attrs.update({'class': 'form-control'})
        return render(request, "cadastrarLocal.html", {'form':form,'status':0})
    else:
        details = localFormCadastro(request.POST)
        if details.is_valid():
            details.save()
            form=localFormCadastro
            
            
            return render(request, "cadastrarLocal.html", {'form':form,'status':1})
        else:
            return render(request, "cadastrarLocal.html", {'form':details}) 


def listarLocais(request):
 
    if request.method=="GET":
        form = Local_instalacao.objects.all()
        return render(request, "listarLocais.html", {'form':form,'status':0}) 

