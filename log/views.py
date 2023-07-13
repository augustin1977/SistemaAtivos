from django.shortcuts import render
from django.contrib.staticfiles.views import serve
from django.http import HttpResponse
from equipamentos.models import Usuario,Tipo,Equipamento,Material_consumo,Media,Fabricante
from .models import *
from django.db.models import Q
from log.models import Log
from django.shortcuts import redirect 
from cadastro_equipamentos import settings
from django.http import HttpResponse, Http404
from os import path
import csv
import codecs
from django.utils import timezone
from cadastro_equipamentos.settings import TIME_ZONE
from datetime import datetime,timedelta
import pytz





from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

lista_transacoes={'eq':'Equipamento','te':'Tipo Equipamento','fn':'Fornecedor','li':'Local Instalação','mc':'Material Consumo',
                        'me':'media','dc':'Disciplina de Manutenção','mf':'Modo de Falha','mq':'Modo de falha Equipamento',
                        'nm':'Ocorrência Material','ne':'Ocorrência Equipamento','us':'usuario','tu':'Tipo de Usuario','rt':"Relatório"}
lista_movimentos={'cd':'Cadastro','lt':'Listagem','ed':'Edição','dl':'Delete','lo':'logon','lf':'logoff'}


def relatorioLog(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    usuario=Usuario.objects.get(id=request.session.get('usuario'))
    #print(f"{Usuario.objects.get(id=usuario.id)} acessou Relatório de Logs")
    #log=Log(transacao='rt',movimento='lt',usuario=Usuario.objects.get(id=usuario.id),alteracao=f'{usuario.nome} visualisou relatório de logs')
    #log.save()
    try :
        tempo=int(request.GET.get("tempo"))
    except:
        tempo=60*6
    date_limit = timezone.now() - timezone.timedelta(days=tempo)
    log=Log.objects.filter(data_cadastro__gte=date_limit).order_by('-data_cadastro')
    lognovo=[]
    for i,item in enumerate(log):
        try:
            lognovo.append({'id':i+1,'transacao':lista_transacoes[item.transacao],'movimento':lista_movimentos[item.movimento],
            'data_cadastro':item.data_cadastro,'usuario':item.usuario,'equipamento':item.equipamento,
            'ocorrencia_equipamento':item.nota_equipamento,'alteracao':item.alteracao})
        except:
            lognovo.append({'id':i+1,'transacao':"Erro",'movimento':"Erro",
            'data_cadastro':item.data_cadastro,'usuario':item.usuario,'equipamento':"Erro",
            'ocorrencia_equipamento':"Erro",'alteracao':item.alteracao})
    return render(request, "relatorioLog.html", {'lista_log':lognovo}) 

def baixarRelatorioLog(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    try :
        tempo=int(request.GET.get("tempo"))
    except:
        tempo=60
    if tempo>0:
        date_limit = timezone.now() - timezone.timedelta(days=tempo)
        log=Log.objects.filter(data_cadastro__gte=date_limit).order_by('-data_cadastro')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio.csv"'
        # Criar um objeto CSV Writer
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response, delimiter=';')
        # Escrever o cabeçalho do arquivo CSV
        writer.writerow(['Data', 'Transação', 'Movimento','Equipamento','Ocorrência','Usuario','Alteração'])
        # Executar a consulta no banco de dados e adicione os resultados ao arquivo CSV
        for obj in log:
            writer.writerow([obj.data_cadastro, obj.transacao, obj.movimento,obj.equipamento,obj.nota_equipamento,
                obj.usuario,obj.alteracao])
        return response
    else:
        data_inicio = datetime.strptime(request.GET.get("dataInicio"), "%Y-%m-%d")
        data_fim = datetime.strptime(request.GET.get("dataFim"), "%Y-%m-%d") + timedelta(days=1)
        filtro1=Q(data_cadastro__gte=data_inicio)
        filtro2=Q(data_cadastro__lte=data_fim)
        log=Log.objects.filter(filtro1 & filtro2).order_by('-data_cadastro')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio.csv"'
        # Criar um objeto CSV Writer
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response, delimiter=';')
        # Escrever o cabeçalho do arquivo CSV
        writer.writerow(['Data', 'Transação', 'Movimento','Equipamento','Ocorrência','Usuario','Alteração'])
        # Executar a consulta no banco de dados e adicione os resultados ao arquivo CSV
        for obj in log:
            writer.writerow([obj.data_cadastro.strftime("%d-%m-%Y %H:%M:%S"), obj.transacao, obj.movimento,obj.equipamento,obj.nota_equipamento,
                obj.usuario,obj.alteracao])
        return response


def relatorioNotasData(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    if request.method=="GET":
        utc=pytz.timezone(TIME_ZONE)
        hoje=utc.localize(datetime.combine((datetime.today()), datetime.min.time()))
        inicio=str(hoje.date()- timedelta(days=1))
        return render(request,'relatorioNotasData.html',{'data_inicio':str(inicio), 'data_fim':str(hoje.date()),'selected':0})
    else:
        utc=pytz.timezone(TIME_ZONE)
     
        datainicio=utc.localize(datetime.combine(datetime.strptime(request.POST.get("data_inicio"),'%Y-%m-%d').date(),datetime.min.time()))
        datafim=utc.localize(datetime.combine(datetime.strptime(request.POST.get("data_fim"),'%Y-%m-%d').date(),datetime.min.time()))
        data_fim =datafim+ timedelta(days=1)
        filtro1=Q(data_ocorrencia__gte=datainicio)
        filtro2=Q(data_ocorrencia__lte=data_fim)
        notas=Nota_equipamento.objects.filter(filtro1 & filtro2).order_by('-data_cadastro')
        # print(notas)

        return render(request,'relatorioNotasData.html',{'form':notas,'data_inicio':str(datainicio.date()), 'data_fim':str(datafim.date()),'selected':0})

def relatorioLogEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    if request.method=="GET":
        equipamento=Equipamento.objects.filter(ativo=True)
        return render(request,'relatorioLogEquipamento.html',{'form':equipamento, 'lista_log':[],'selected':0})
    else:
        equipamentoid=request.POST.get('equipamento')
        log=Log.objects.filter(equipamento=equipamentoid).order_by('-data_cadastro')
        equipamento=Equipamento.objects.filter(ativo=True)
        lognovo=[]
        for i,item in enumerate(log):
            try:
                lognovo.append({'id':i+1,'transacao':lista_transacoes[item.transacao],'movimento':lista_movimentos[item.movimento],
                'data_cadastro':item.data_cadastro,'usuario':item.usuario,'equipamento':item.equipamento,
                'ocorrencia_equipamento':item.nota_equipamento,'alteracao':item.alteracao})
            except:
                lognovo.append({'id':i+1,'transacao':"Erro",'movimento':"Erro",
                'data_cadastro':item.data_cadastro,'usuario':item.usuario,'equipamento':"Erro",
                'ocorrencia_equipamento':"Erro",'alteracao':item.alteracao})
        return render(request,'relatorioLogEquipamento.html',{'form':equipamento, 'lista_log':lognovo,'selected':int(equipamentoid)})
    return HttpResponse("Parcialmente implementado")

def baixarRelatorioLogEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    try :
        teste=int(request.GET.get("equipamentoid"))
    except:
        teste=0
    log=Log.objects.filter(equipamento=teste).order_by('-data_cadastro')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio.csv"'
    # Criar um objeto CSV Writer
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=';')
    # Escrever o cabeçalho do arquivo CSV
    writer.writerow(['Data', 'Transação', 'Movimento','Equipamento','Ocorrência','Usuario','Alteração'])
    # Executar a consulta no banco de dados e adicione os resultados ao arquivo CSV   
    for obj in log:
        writer.writerow([obj.data_cadastro, obj.transacao, obj.movimento,obj.equipamento,obj.nota_equipamento,
            obj.usuario,obj.alteracao])
    return response

def menuRelatorios(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    # cria a view do login do usuário
    status=str(request.GET.get('status'))
    return render(request, "homeRelatorio.html", {'status':status})

def relatorioNotasEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    if request.method=="GET":
        equipamento=Equipamento.objects.filter(ativo=True)
        return render(request,'relatorioNotasEquipamento.html',{'form':equipamento, 'lista_notas':[],'selected':0})
    else:
        equipamentoid=request.POST.get('equipamento')
        notas=Nota_equipamento.objects.filter(equipamento=equipamentoid).order_by('-data_cadastro')
        equipamento=Equipamento.objects.filter(ativo=True)
        return render(request,'relatorioNotasEquipamento.html',{'form':equipamento, 'lista_notas':notas,'selected':int(equipamentoid)})
    return HttpResponse("Parcialmente implementado")

def baixarRelatorioNotaEquipamento(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    try :
        busca=int(request.GET.get("equipamentoid"))
    except:
        busca=0
        
    notas=Nota_equipamento.objects.filter(equipamento=busca).order_by('-data_cadastro')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio.csv"'
    # Criar um objeto CSV Writer
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=';')
    # Escrever o cabeçalho do arquivo CSV
    writer.writerow(['Data_ocorrencia','Data_cadastro', 'Titulo', 'Descrição','Equipamento','Usuario'])
    # Executar a consulta no banco de dados e adicione os resultados ao arquivo CSV   
    for obj in notas:
        writer.writerow([obj.data_ocorrencia, obj.data_cadastro, obj.titulo,obj.descricao,obj.equipamento,
            obj.usuario])
    return response

def relatorioLogData(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    if request.method=="GET":
        utc=pytz.timezone(TIME_ZONE)
        hoje=utc.localize(datetime.combine((datetime.today()), datetime.min.time()))
        inicio=inicio=str(hoje.date()- timedelta(days=1))
        log=[]
   
        return render(request,'relatorioLogData.html',{'lista_log':log,'data_inicio':inicio, 'data_fim':str(hoje.date()),'selected':0})
    else:
        utc=pytz.timezone(TIME_ZONE)
     
        datainicio=utc.localize(datetime.combine(datetime.strptime(request.POST.get("data_inicio"),'%Y-%m-%d').date(),datetime.min.time()))
        datafim=utc.localize(datetime.combine(datetime.strptime(request.POST.get("data_fim"),'%Y-%m-%d').date(),datetime.min.time()))
        data_fim =datafim+ timedelta(days=1)

        filtro1=Q(data_cadastro__gte=datainicio)
        filtro2=Q(data_cadastro__lte=data_fim)
        log=Log.objects.filter(filtro1 & filtro2).order_by('-data_cadastro')
        #print(notas)
        lognovo=[]
        for i,item in enumerate(log):
            try:
                lognovo.append({'id':i+1,'transacao':lista_transacoes[item.transacao],'movimento':lista_movimentos[item.movimento],
                'data_cadastro':item.data_cadastro,'usuario':item.usuario,'equipamento':item.equipamento,
                'ocorrencia_equipamento':item.nota_equipamento,'alteracao':item.alteracao})
            except:
                lognovo.append({'id':i+1,'transacao':"Erro",'movimento':"Erro",
                'data_cadastro':item.data_cadastro,'usuario':item.usuario,'equipamento':"Erro",
                'ocorrencia_equipamento':"Erro",'alteracao':item.alteracao})
        return render(request,'relatorioLogData.html',{'lista_log':lognovo,'data_inicio':str(datainicio.date()), 'data_fim':str(datafim.date()),'selected':0})
    
def baixarRelatorionotasEquipamentodata(request):

    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    try :
        datai=(request.GET.get("data_inicio"))
        dataf=(request.GET.get("data_fim"))
    except:
        datai=0
        dataf=0
    filtro1=Q(data_ocorrencia__gte=datai)
    filtro2=Q(data_ocorrencia__lte=dataf)
    notas=Nota_equipamento.objects.filter(filtro1 & filtro2).order_by('-data_cadastro')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio.csv"'
    # Criar um objeto CSV Writer
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=';')
    # Escrever o cabeçalho do arquivo CSV
    writer.writerow(['Data_ocorrencia','Data_cadastro', 'Titulo', 'Descrição','Equipamento','Usuario'])
    # Executar a consulta no banco de dados e adicione os resultados ao arquivo CSV   
    for obj in notas:
        writer.writerow([obj.data_ocorrencia, obj.data_cadastro, obj.titulo,obj.descricao,obj.equipamento,
            obj.usuario])
    return response


def baixarRelatorioLogPDF(request):
    if not request.session.get('usuario'):
        return redirect('/auth/login/?status=2')
    try:
        tempo = int(request.GET.get("tempo"))
    except:
        tempo = 60

    if tempo > 0:
        date_limit = timezone.now() - timezone.timedelta(days=tempo)
        log = Log.objects.filter(data_cadastro__gte=date_limit).order_by('-data_cadastro')
    else:
        utc=pytz.timezone(TIME_ZONE)
        data_inicio=utc.localize(datetime.combine(datetime.strptime(request.GET.get("dataInicio"),'%Y-%m-%d').date(),datetime.min.time()))
        data_fim=utc.localize(datetime.combine(datetime.strptime(request.GET.get("dataFim"),'%Y-%m-%d').date(),datetime.min.time())+ timedelta(days=1))
        #data_inicio =datetime.strptime(request.GET.get("dataInicio"), "%Y-%m-%d")
        #data_fim = datetime.strptime(request.GET.get("dataFim"), "%Y-%m-%d") + timedelta(days=1)
        
        filtro1 = Q(data_cadastro__gte=data_inicio)
        filtro2 = Q(data_cadastro__lte=data_fim)
        log = Log.objects.filter(filtro1 & filtro2).order_by('-data_cadastro')

    # Criar o objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

   # Cabeçalho personalizado
    styles = getSampleStyleSheet()
    header_style = styles['Heading1']
    header_text = 'Sistema de Gestão de Ativos - LPM'
    header_paragraph_style = ParagraphStyle('HeaderParagraphStyle', parent=header_style, alignment=1, fontSize=14)
    elements.append(Paragraph(header_text, header_paragraph_style))

    subheader_style = styles['Heading2']
    subheader_text = 'Relatório de LOG por data'
    subheader_paragraph_style = ParagraphStyle('SubheaderParagraphStyle', parent=subheader_style, alignment=1, fontSize=12)
    elements.append(Paragraph(subheader_text, subheader_paragraph_style))

    # Informações de data
    date_style = ParagraphStyle('DateStyle', parent=styles['Normal'], spaceAfter=12)
    date_today = datetime.now().strftime("%d/%m/%Y %H:%M")
    date_start = data_inicio.strftime("%d/%m/%Y")
    date_end = (data_fim - timedelta(days=1)).strftime("%d/%m/%Y")
    usuario_relatorio= str(Usuario.objects.get(id=request.session.get('usuario')))
    date_info = f'Relatório emitido por {usuario_relatorio} em {date_today}<br/>Data de início do filtro: {date_start} Data de fim do filtro: {date_end}'
    elements.append(Paragraph(date_info, date_style))

    # Tabela com os dados
    table_data = [['Data', 'Transação', 'Movimento', 'Equipamento', 'Ocorrência', 'Usuário', 'Alteração']]
    for obj in log:
        if obj.equipamento==None:
            equipamento=""
        else:
            equipamento=str(obj.equipamento)
        if obj.nota_equipamento==None:
            nota=""
        else:
            nota=str(obj.nota_equipamento)
        usuario=str(obj.usuario)
        row = [
            Paragraph(obj.data_cadastro.strftime("%d-%m-%Y %H:%M:%S"), styles['Normal']),
            Paragraph(lista_transacoes[obj.transacao], styles['Normal']),
            Paragraph(lista_movimentos[obj.movimento], styles['Normal']),
            Paragraph(equipamento, styles['Normal']),
            Paragraph(nota, styles['Normal']),
            Paragraph(usuario, styles['Normal']),
            Paragraph(obj.alteracao, styles['Normal']),
        ]      
        table_data.append(row)
    table_style = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
      # Definir a largura das colunas
    col_widths = [0.9* inch, 1 * inch, 0.8 * inch, 1* inch, 1 * inch, 1 * inch, 2 * inch]
    table = Table(table_data, colWidths=col_widths,repeatRows=1)
    table.setStyle(table_style)
    elements.append(table)

    # Construir o documento PDF
    def rodape(canvas, doc):
        numero_pagina = canvas.getPageNumber()
        texto = f"Página {numero_pagina}"
        canvas.saveState()
        canvas.setFont("Helvetica", 10)
        canvas.drawString(inch, 0.75 * inch, texto)
        canvas.restoreState()

    # Associar a função de rodapé ao documento
    doc.build(
        elements,onFirstPage=rodape,
        onLaterPages=rodape
    )
    return response
