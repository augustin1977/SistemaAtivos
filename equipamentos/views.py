from django.shortcuts import render

from django.http import HttpResponse
from .models import Usuario,Tipo,Equipamento
from django.shortcuts import redirect 
from hashlib import sha256
import re
def home(request):
    # cria a view do login do usuário
    status=str(request.GET.get('status'))
    return render(request, "home.html", {'status':status})
def lista_equipamentos(request):
    equipamentos=Equipamento.objects.all()
    return render(request, "exibirEquipamentos.html", {'equipamentos':equipamentos})
