from django.shortcuts import render
from django.contrib.staticfiles.views import serve
from django.http import HttpResponse
from equipamentos.models import Usuario,Tipo,Equipamento,Material_consumo,Media,Fabricante
from log.models import Log
from django.shortcuts import redirect 
from hashlib import sha256
from cadastro_equipamentos import settings
from django.http import HttpResponse, Http404
from os import path

lista_transacoes=[('eq','Equipamento'),('te','Tipo Equipamento'),('fn','Fornecedor'),('li','Local Instalação'),('mc','Material Consumo'),
                        ('me','media'),('dc','Disciplina de Manutenção'),('mf','Modo de Falha'),('me','Modo de falha Equipamento'),
                        ('nm','Nota Material'),('ne','Nota Equipamento'),('us','usuario'),('tu','Tipo de Usuario'),("rt","Relatório")]
lista_movimentos=[('cd','Cadastro'),('lt','Listagem'),('ed','Edição'),('dl','Delete'),('lo','logOn'),('lf','logOff')]
def listarLog(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    print(f"{Usuario.objects.get(id=usuario.id)} acessou Relatório de Logs")
    log=Log(transacao='rt',movimento='lt',usuario=Usuario.objects.get(id=usuario.id),alteracao=f'{usuario.nome} visualisou relatório de logs')
    log.save()
    log=Log.objects.all().order_by('-data_cadastro')[:200]
    lognovo=[]
    for i,item in enumerate(log):
        lognovo.append({'id':i+1,'transacao':lista_transacoes[item.transacao],'movimento':lista_movimentos[item.movimento],
            'data_cadastro':item.data_cadastro,'usuario':item.usuario,'equipamento':item.equipamento,
            'nota_equipamento':item.nota_equipamento,'alteracao':item.alteracao})
    return render(request, "relatorioLog.html", {'lista_log':lognovo}) 

