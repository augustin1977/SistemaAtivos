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
            print('valido')
            data=form.cleaned_data
            disciplina=Disciplina(disciplina=data['disciplina'])
            disciplina.save()
            form=cadastraDisciplinaForm
                        
            return render(request, "cadastrarDisciplina.html", {'form':form,'status':1})
        else:
            print('invalido')
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
            print('valido')
            data=form.cleaned_data
            disciplina=Modo_Falha(disciplina=data['disciplina'],modo_falha=data['modo_falha'])
            disciplina.save()
            form=CadastraModo_FalhaForm
                        
            return render(request, "cadastrarModo_Falha.html", {'form':form,'status':1})
        else:
            print('invalido')
            return render(request, "cadastrarModo_Falha.html", {'form':form}) 