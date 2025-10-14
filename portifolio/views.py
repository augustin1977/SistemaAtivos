from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from usuarios.autentica_usuario import *
from .models import *
from .forms import *

@is_superuser
def cadastra_cores(request):
    status = 0
    if request.method == 'POST':
        form = CorForm(request.POST)
        if form.is_valid():
            Cor.objects.create(
                nome=form.cleaned_data['nome'],
                tonalidade=form.cleaned_data['tonalidade'],
                ativa=form.cleaned_data.get('ativa', False),
            )
            status = 1
            form = CorForm()  # limpa o formulário após sucesso
    else:
        form = CorForm()
    return render(request, 'cadastra_cores.html', {'form': form, 'status': status})

@is_user
def exibe_cores(request):
    cores = Cor.objects.all().order_by('nome')
    return render(request, 'exibe_cores.html', {'cores': cores})
@is_superuser
def edita_cores(request,id):
    cor = get_object_or_404(Cor, id=id)
    status = 0

    if request.method == 'POST':
        form = CorForm(request.POST)
        if form.is_valid():
            cor.nome = form.cleaned_data['nome']
            cor.tonalidade = form.cleaned_data['tonalidade']
            cor.ativa = form.cleaned_data.get('ativa', False)
            cor.save()
            status = 1
    else:
        form = CorForm(initial={
            'id': cor.id,
            'nome': cor.nome,
            'tonalidade': cor.tonalidade,
            'ativa': cor.ativa,
        })
    return render(request, 'cadastra_cores.html', {'form': form, 'status': status})

@is_admin
def deleta_cores(request,id):
    cor = get_object_or_404(Cor, id=id)
    if request.method == 'POST':
        cor.delete()
        return redirect('exibe_cores')
    return render(request, 'confirma_exclusao.html', {'cor': cor})

@is_user
def cadastra_projetos(request):
    pass
@is_user
def exibe_projetos(request):
    pass
@is_user
def edita_projetos(request):
    pass
@is_superuser
def deleta_projetos(request):
    pass
@is_user
def cadastra_amostras(request):
    pass
@is_user
def exibe_amostras(request):
    pass
@is_user
def edita_amostras(request):
    pass
@is_user
def deleta_amostras(request):
    pass
@is_user
def cadastra_etiquetas(request):
    pass
@is_user
def exibe_etiquetas(request):
    pass
@is_user
def edita_etiquetas(request):
    pass
@is_user
def deleta_etiquetas(request):
    pass
@is_user
def imprime_etiquetas(request):
    pass

