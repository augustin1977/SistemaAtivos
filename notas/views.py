from django.shortcuts import render
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
# adicionando 