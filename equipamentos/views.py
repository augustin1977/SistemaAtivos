from django.shortcuts import render

from django.http import HttpResponse
from .models import Usuario,Tipo,Equipamento,Material_consumo
from django.shortcuts import redirect 
from hashlib import sha256
import re
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
    return render(request, "exibirDetalheEquipamento.html", {'equipamento':equipamento, 'materiais':materiais})