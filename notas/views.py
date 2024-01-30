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
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def notas(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    # cria a view do login do usuário
    status=str(request.GET.get('status'))
    return render(request, "notas.html", {'status':status})

def cadastrarDisciplina(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    #print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou cadastro cadastro Disciplina")
    
    # verificado o tipo de usuario - controle de acesso a algumas funções
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo1=Q(tipo="superuser")
    tipo2=Q(tipo='especialuser')
    tipo3=Q(tipo='admin')

    tipo=Tipo.objects.filter(tipo1 | tipo2 | tipo3)
    if(usuario.tipo not in tipo):
          return redirect(f'/equipamentos/?status=50')

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
            Log.cadastramento(usuario=Usuario.objects.get(id=request.session.get('usuario')),transacao='dc',objeto=disciplina)
            form=cadastraDisciplinaForm
                        
            return render(request, "cadastrarDisciplina.html", {'form':form,'status':1})
        else:
            return render(request, "cadastrarDisciplina.html", {'form':details}) 
       
def cadastrarModo_Falha(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    #print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou cadastro cadastro Modo de Falha")
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo1=Q(tipo="superuser")
    tipo2=Q(tipo='especialuser')
    tipo3=Q(tipo='admin')

    tipo=Tipo.objects.filter(tipo1 | tipo2 | tipo3)
    if(usuario.tipo not in tipo):
          return redirect(f'/equipamentos/?status=50')
    
    if request.method=="GET":
        form=CadastraModo_FalhaForm
        return render(request, "cadastrarModo_Falha.html", {'form':form,'status':0})
    else:
        details = (request.POST)
        form=CadastraModo_FalhaForm(details)
        if form.is_valid():
            data=form.cleaned_data
            modofalha=Modo_Falha(disciplina=data['disciplina'],modo_falha=data['modo_falha'])
            modofalha.save()
            Log.cadastramento(usuario=Usuario.objects.get(id=request.session.get('usuario')),transacao='mf',objeto=modofalha)
            form=CadastraModo_FalhaForm
                        
            return render(request, "cadastrarModo_Falha.html", {'form':form,'status':1})
        else:
            return render(request, "cadastrarModo_Falha.html", {'form':form}) 

def cadastrarModo_FalhaEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    #print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou cadastro cadastro Modo de Falha Equipamento")
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo1=Q(tipo="superuser")
    tipo2=Q(tipo='especialuser')
    tipo3=Q(tipo='admin')

    tipo=Tipo.objects.filter(tipo1 | tipo2 | tipo3)
    if(usuario.tipo not in tipo):
          return redirect(f'/equipamentos/?status=50')
    
    
    if request.method=="GET":
        form=CadastraModo_falha_equipamentoForm
        return render(request, "cadastrarModoFalhaEquipamento.html", {'form':form,'status':0})
    else:
        details = (request.POST)
        form=CadastraModo_falha_equipamentoForm(details)
        if form.is_valid():
            data=form.cleaned_data
            modofalhaequipamento=Modo_falha_equipamento(equipamento=data['equipamento'],modo_falha=data['modo_falha'])
            modofalhaequipamento.save()
            Log.cadastramento(usuario=Usuario.objects.get(id=request.session.get('usuario')),transacao='me',objeto=modofalhaequipamento)
            form=CadastraModo_falha_equipamentoForm
                        
            return render(request, "cadastrarModoFalhaEquipamento.html", {'form':form,'status':1})
        else:
            return render(request, "cadastrarModoFalhaEquipamento.html", {'form':form}) 
       
def cadastrarNota(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    #print(f"{usuario.nome} acessou cadastro Notas")
    if request.method=="GET":
        form=CadastraNota_equipamentoForm
        return render(request, "cadastrarNota.html", {'form':form,'status':0})
    else:
        details = (request.POST)
        form=CadastraNota_equipamentoForm(details)
        if form.is_valid():
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
            # Linhas comentadas até a conclusão do cadastramento de material de consumo
            """for material in data['material']:
                #Nota_material
                nota.material.add(material)
            """    
            Log.cadastramento(usuario=Usuario.objects.get(id=request.session.get('usuario')),transacao='ne',objeto=nota,nota_equipamento=nota)
            form=CadastraNota_equipamentoForm
            
            return render(request, "cadastrarNota.html", {'form':form,'status':1})
        else:
            #print('invalido')
            return render(request, "cadastrarNota.html", {'form':form}) 

def get_modos_de_falha(request):
    equipamento_id = request.GET.get('equipamento_id')
    modos_falha = Modo_falha_equipamento.objects.filter(equipamento_id=equipamento_id).values('id', 'modo_falha')
    modos_falha=list(modos_falha)
    
    for modo_falha in modos_falha:
        modo_falha['modo_falha']=str(Modo_Falha.objects.get(id=modo_falha['modo_falha'])) 
    return JsonResponse(modos_falha, safe=False)

def excluirDisciplina(request):
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo1=Q(tipo="superuser")
    tipo2=Q(tipo='especialuser')
    tipo3=Q(tipo='admin')

    tipo=Tipo.objects.filter(tipo1 | tipo2 | tipo3)
    if(usuario.tipo not in tipo):
          return redirect(f'/equipamentos/?status=50')
    return HttpResponse("<h1>Não implementado</h1>")

def editarDisciplina(request):
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo1=Q(tipo="superuser")
    tipo2=Q(tipo='especialuser')
    tipo3=Q(tipo='admin')

    tipo=Tipo.objects.filter(tipo1 | tipo2 | tipo3)
    if(usuario.tipo not in tipo):
          return redirect(f'/equipamentos/?status=50')
    return HttpResponse("<h1>Acesso não autorizado</h1>")

def exibirDisciplinas(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    disciplinas=Disciplina.objects.all()
    return render(request, "exibirDisciplinas.html", {'disciplinas':disciplinas,'status':0})

def excluirModoFalha(request):
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo1=Q(tipo="superuser")
    tipo2=Q(tipo='especialuser')
    tipo3=Q(tipo='admin')

    tipo=Tipo.objects.filter(tipo1 | tipo2 | tipo3)
    if(usuario.tipo not in tipo):
          return redirect(f'/equipamentos/?status=50')
    return HttpResponse("<h1>Não implementado</h1>")

def editarModoFalha(request):
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo1=Q(tipo="superuser")
    tipo2=Q(tipo='especialuser')
    tipo3=Q(tipo='admin')

    tipo=Tipo.objects.filter(tipo1 | tipo2 | tipo3)
    if(usuario.tipo not in tipo):
          return redirect(f'/equipamentos/?status=50')
    return HttpResponse("<h1>Acesso não autorizado</h1>")

def exibirModoFalha(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    modosFalha=Modo_Falha.objects.all()
    
    return render(request, "exibirModosFalha.html", {'modosFalha':modosFalha,'status':0})

def excluirModoFalhaEquipamento(request):
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo1=Q(tipo="superuser")
    tipo2=Q(tipo='especialuser')
    tipo3=Q(tipo='admin')

    tipo=Tipo.objects.filter(tipo1 | tipo2 | tipo3)
    if(usuario.tipo not in tipo):
          return redirect(f'/equipamentos/?status=50')
    return HttpResponse("<h1>Não implementado</h1>")

def editarModoFalhaEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    tipo1=Q(tipo="superuser")
    tipo2=Q(tipo='especialuser')
    tipo3=Q(tipo='admin')

    tipo=Tipo.objects.filter(tipo1 | tipo2 | tipo3)
    if(usuario.tipo not in tipo):
          return redirect(f'/equipamentos/?status=50')
    
    return HttpResponse("<h1>Acesso não autorizado</h1>") 
    # linha inserida para evitar execução do codigo abaixo, deve ser refeita essa rotina a luz de novos entendimento
    # perguntas=[{'numero':1,'texto':"É ligado na energia?","resposta":"resposta1",'sim':'sim1','nao':'nao1'},
    #         {'numero':2,'texto':"Tem partes eletronicas?","resposta":"resposta2",'sim':'sim2','nao':'nao2'},
    #         {'numero':3,'texto':"Tem alguns sistema hidraulico?","resposta":"resposta3",'sim':'sim3','nao':'nao3'},
    #         {'numero':4,'texto':"Tem partes moveis?","resposta":"resposta4",'sim':'sim4','nao':'nao4'},
    #         {'numero':5,'texto':"Necessita base Civil?","resposta":"resposta5",'sim':'sim5','nao':'nao5'},
    #         {'numero':6,'texto':"Tem controlador ou PLC?","resposta":"resposta6",'sim':'sim6','nao':'nao6'},
    #         {'}numero':7,'texto':"é conectado a uma computador ou é microprocessado?","resposta":"resposta7",'sim':'sim7','nao':'nao7'},]
    # lista=[]
    # for r in perguntas:
    #     lista.append(r['resposta'])
    # if request.method=="GET":      
        
        
    #     mf=Modo_falha_equipamento.objects.get(id=request.GET.get('id'))
    #     equipamento=mf.equipamento
    #     modosFalha=Modo_falha_equipamento.objects.filter(equipamento=equipamento)
    #     return  render(request, "editarModoFalhaEquipamento.html",
    #                     {'modosFalha':modosFalha,'perguntas':perguntas,'equipamento':equipamento,'status':0})
    

    # equipamento=Equipamento.objects.get(id=request.POST.get('id')) 
    # modosFalha=Modo_falha_equipamento.objects.filter(equipamento=equipamento)
    
    # respostas=[]                 
    # for l in lista:
    #     res=request.POST.get(l)
    #     if res=='1':
    #         respostas.append(True)
    #     elif res=='0':
    #         respostas.append(False)
    #     else:
    #         respostas.append(None)   
        
    # resposta="-".join( str(valor) for valor in respostas)

    # return redirect('/notas/exibirModoFalhaEquipamento')

def exibirModoFalhaEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    modosFalha=Modo_falha_equipamento.objects.all()
    paginator = Paginator(modosFalha, 25) # paginando resultados
    #log=Log(transacao='eq',movimento='lt',usuario=usu,alteracao=f'{usu.nome} visualisou Lista equipamentos') # depois tem que logar isso
    page = request.GET.get('page')# verifica se ja tem um pagina escolhida
    try:
        resultados_paginados = paginator.get_page(page) # cria paginas
    except PageNotAnInteger:
        # Se o número da página não for um inteiro, mostre a primeira página
        resultados_paginados = paginator.get_page(1)
    except EmptyPage:
        # Se o número da página estiver fora do intervalo, mostre a última página
        resultados_paginados = paginator.get_page(paginator.num_pages)
    
    return render(request, "exibirModosFalhaEquipamento.html", {'modosFalha':resultados_paginados,'status':0})

def exibirNotas(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    notas = Nota_equipamento.objects.order_by('-data_ocorrencia', '-data_cadastro')# se quiser criar filtro é aqui que deve fazer isso
    paginator = Paginator(notas, 25) # paginando resultados
    #log=Log(transacao='eq',movimento='lt',usuario=usu,alteracao=f'{usu.nome} visualisou Lista equipamentos') # depois tem que logar isso
    page = request.GET.get('page')# verifica se ja tem um pagina escolhida
    try:
        resultados_paginados = paginator.get_page(page) # cria paginas
    except PageNotAnInteger:
        # Se o número da página não for um inteiro, mostre a primeira página
        resultados_paginados = paginator.get_page(1)
    except EmptyPage:
        # Se o número da página estiver fora do intervalo, mostre a última página
        resultados_paginados = paginator.get_page(paginator.num_pages)
    
    
    return render(request, "exibirnotas.html", {'notas':resultados_paginados})

def editarNotas(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    ##print(f"{usuario.nome} acessou edição Notas")
    if request.method=="GET":
        id=request.GET.get('id')
        nota= get_object_or_404(Nota_equipamento, pk=id)
        ##print(nota)
        form=CadastraNota_equipamentoForm(instance=nota)
        if form.is_valid():
            pass
        return render(request, "editarNota.html", {'form':form,'status':0,'id':id})
    else:
        details = (request.POST)
        form=CadastraNota_equipamentoForm(details)
        if form.is_valid():
            ##print('valido')
            id=request.POST.get('id')

            nota= Nota_equipamento.objects.get(id=id)
            listaCampos=['titulo','descricao','equipamento','modo_Falha_equipamento','data_ocorrencia','falha',
                         'calibracao','lubrificao']
            alteracao=False
            for campo in listaCampos:
                alterado=Log.foiAlterado(transacao='me',objeto=nota,atributo=campo,valor=form.cleaned_data[campo],usuario=usuario,nota_equipamento=nota) 
                if alterado:
                    setattr(nota,campo,form.cleaned_data[campo])
                alteracao|=alterado
            if alteracao:
                nota.usuario=usuario
                nota.save() 

            form=CadastraNota_equipamentoForm
            return redirect("/notas/exibirNotas")
        else:
            ##print('invalido')
            return render(request, "editarNota.html", {'form':form})    

def excluirNotas(request):
    return HttpResponse("<h1>Acesso não autorizado</h1>")
    return HttpResponse("<h1>Não implementado</h1>")