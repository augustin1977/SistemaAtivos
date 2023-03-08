from django.shortcuts import render, get_object_or_404
from equipamentos.models import *
from .models import *
from django.contrib.staticfiles.views import serve
from django.http import HttpResponse
from django.shortcuts import redirect 
from cadastro_equipamentos import settings
from django.http import HttpResponse, Http404
from os import path
import urllib.request
from cadastro_equipamentos.settings import BASE_DIR,MEDIA_ROOT,TIME_ZONE
import os,csv
from log.models import Log
from .forms import *
from django.http import JsonResponse



def notas(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    # cria a view do login do usuário
    status=str(request.GET.get('status'))
    return render(request, "notas.html", {'status':status})

def cadastrarDisciplina(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou cadastro cadastro Disciplina")
    if request.method=="GET":
        form=cadastraDisciplinaForm
        return render(request, "cadastrarDisciplina.html", {'form':form,'status':0})
    else:
        details = (request.POST)
        form=cadastraDisciplinaForm(details)
        if form.is_valid():
            data=form.cleaned_data
            disciplina=Disciplina(disciplina=data['disciplina'])
            disciplina.save()
            form=cadastraDisciplinaForm
                        
            return render(request, "cadastrarDisciplina.html", {'form':form,'status':1})
        else:
            return render(request, "cadastrarDisciplina.html", {'form':details}) 

        
def cadastrarModo_Falha(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou cadastro cadastro Modo de Falha")
    if request.method=="GET":
        form=CadastraModo_FalhaForm
        return render(request, "cadastrarModo_Falha.html", {'form':form,'status':0})
    else:
        details = (request.POST)
        form=CadastraModo_FalhaForm(details)
        if form.is_valid():
            data=form.cleaned_data
            disciplina=Modo_Falha(disciplina=data['disciplina'],modo_falha=data['modo_falha'])
            disciplina.save()
            form=CadastraModo_FalhaForm
                        
            return render(request, "cadastrarModo_Falha.html", {'form':form,'status':1})
        else:
            return render(request, "cadastrarModo_Falha.html", {'form':form}) 

def cadastrarModo_FalhaEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou cadastro cadastro Modo de Falha Equipamento")
    if request.method=="GET":
        form=CadastraModo_falha_equipamentoForm
        return render(request, "cadastrarModoFalhaEquipamento.html", {'form':form,'status':0})
    else:
        details = (request.POST)
        form=CadastraModo_falha_equipamentoForm(details)
        if form.is_valid():
            data=form.cleaned_data
            disciplina=Modo_falha_equipamento(equipamento=data['equipamento'],modo_falha=data['modo_falha'])
            disciplina.save()
            form=CadastraModo_falha_equipamentoForm
                        
            return render(request, "cadastrarModoFalhaEquipamento.html", {'form':form,'status':1})
        else:
            return render(request, "cadastrarModoFalhaEquipamento.html", {'form':form}) 
       
def cadastrarNota(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    print(f"{usuario.nome} acessou cadastro Notas")
    if request.method=="GET":
        form=CadastraNota_equipamentoForm
        return render(request, "cadastrarNota.html", {'form':form,'status':0})
    else:
        details = (request.POST)
        form=CadastraNota_equipamentoForm(details)
        if form.is_valid():
            print('valido')
            data=form.cleaned_data
            
            nota=Nota_equipamento(
                titulo=data['titulo'],
                descricao=data['descricao'],
                equipamento=data['equipamento'],
                modo_Falha_equipamento=data['modo_Falha_equipamento'],
                data_cadastro=data['data_cadastro'],
                data_ocorrencia=data['data_ocorrencia'],
                falha=data['falha'],
                calibracao=data['calibracao'],
                lubrificao=data['lubrificao'],
                usuario=usuario
            )
            nota.save()
            form=CadastraNota_equipamentoForm
            return render(request, "cadastrarNota.html", {'form':form,'status':1})
        else:
            print('invalido')
            return render(request, "cadastrarNota.html", {'form':form}) 


def get_modos_de_falha(request):
    equipamento_id = request.GET.get('equipamento_id')
    modos_falha = Modo_falha_equipamento.objects.filter(equipamento_id=equipamento_id).values('id', 'modo_falha')
    modos_falha=list(modos_falha)
    
    for modo_falha in modos_falha:
        modo_falha['modo_falha']=str(Modo_Falha.objects.get(id=modo_falha['modo_falha']))
    print(modos_falha)    
    return JsonResponse(modos_falha, safe=False)

def excluirDisciplina(request):
    return HttpResponse(request.GET.get('id'))

def editarDisciplina(request):
    return HttpResponse(request.GET.get('id'))

def exibirDisciplinas(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    disciplinas=Disciplina.objects.all()
    return render(request, "exibirDisciplinas.html", {'disciplinas':disciplinas,'status':0})


def excluirModoFalha(request):
    return HttpResponse(request.GET.get('id'))

def editarModoFalha(request):
    return HttpResponse(request.GET.get('id'))

def exibirModoFalha(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    modosFalha=Modo_Falha.objects.all()
    
    return render(request, "exibirModosFalha.html", {'modosFalha':modosFalha,'status':0})


def excluirModoFalhaEquipamento(request):
    return HttpResponse(request.GET.get('id'))

def editarModoFalhaEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    perguntas=[{'numero':1,'texto':"É ligado na energia?","resposta":"resposta1",'sim':'sim1','nao':'nao1'},
            {'numero':2,'texto':"Tem partes eletronicas?","resposta":"resposta2",'sim':'sim2','nao':'nao2'},
            {'numero':3,'texto':"Usa outra fonte de energia?","resposta":"resposta3",'sim':'sim3','nao':'nao3'},
            {'numero':4,'texto':"Tem partes moveis?","resposta":"resposta4",'sim':'sim4','nao':'nao4'},
            {'numero':5,'texto':"usa combustivel?","resposta":"resposta5",'sim':'sim5','nao':'nao5'},]
    lista=[]
    for r in perguntas:
        lista.append(r['resposta'])
    if request.method=="GET":      
        
        
        mf=Modo_falha_equipamento.objects.get(id=request.GET.get('id'))
        equipamento=mf.equipamento
        modosFalha=Modo_falha_equipamento.objects.filter(equipamento=equipamento)
        return  render(request, "editarModoFalhaEquipamento.html",
                        {'modosFalha':modosFalha,'perguntas':perguntas,'equipamento':equipamento,'status':0})
    
    print(request.POST.get('id'))
    equipamento=Equipamento.objects.get(id=request.POST.get('id')) 
    modosFalha=Modo_falha_equipamento.objects.filter(equipamento=equipamento)
    
    respostas=[]                 
    for l in lista:
        res=request.POST.get(l)
        if res=='1':
            respostas.append(True)
        elif res=='0':
            respostas.append(False)
        else:
            respostas.append(None)   
        
    resposta="-".join( str(valor) for valor in respostas)
    print(modosFalha[0].equipamento, resposta)

    return redirect('/notas/exibirModoFalhaEquipamento')

def exibirModoFalhaEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    modosFalha=Modo_falha_equipamento.objects.all()
    return render(request, "exibirModosFalhaEquipamento.html", {'modosFalha':modosFalha,'status':0})

def exibirNotas(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    notas=Nota_equipamento.objects.all() # depois tenho que filtrar isso
    #log=Log(transacao='eq',movimento='lt',usuario=usu,alteracao=f'{usu.nome} visualisou Lista equipamentos') # depois tem que logar isso
    return render(request, "exibirnotas.html", {'notas':notas})

def editarNotas(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    print(f"{usuario.nome} acessou edição Notas")
    if request.method=="GET":
        id=request.GET.get('id')
        nota= get_object_or_404(Nota_equipamento, pk=id)
        print(nota)
        form=CadastraNota_equipamentoForm(instance=nota)
        if form.is_valid():
            pass
        return render(request, "editarNota.html", {'form':form,'status':0,'id':id})
    else:
        details = (request.POST)
        form=CadastraNota_equipamentoForm(details)
        if form.is_valid():
            print('valido')
            data=form.cleaned_data
            print(data)
            id=request.POST.get('id')
            print(id)
            nota= Nota_equipamento.objects.get(id=id)
            print(nota)
            nota.titulo=data['titulo']
            nota.descricao=data['descricao']
            nota.equipamento=data['equipamento']
            nota.modo_Falha_equipamento=data['modo_Falha_equipamento']
            nota.data_cadastro=data['data_cadastro']
            nota.data_ocorrencia=data['data_ocorrencia']
            nota.falha=data['falha']
            nota.calibracao=data['calibracao']
            nota.lubrificao=data['lubrificao']
            nota.usuario=usuario
            nota.save()
            form=CadastraNota_equipamentoForm
            return redirect("/notas/exibirNotas")
        else:
            print('invalido')
            return render(request, "editarNota.html", {'form':form})    

def excluirNotas(request):
    HttpResponse("<h1>Não implementado</h1>")
