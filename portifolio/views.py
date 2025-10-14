from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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
                nome=form.cleaned_data['nome'].capitalize(),
                tonalidade=form.cleaned_data['tonalidade'].upper(),
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
            cor.nome = form.cleaned_data['nome'].capitalize()
            cor.tonalidade = form.cleaned_data['tonalidade'].upper()
            cor.ativa = form.cleaned_data.get('ativa', False)
            cor.save()
            status = 1
            messages.success(request, f"A cor '{cor.nome}' foi atualizada com sucesso!")
            return redirect("exibe_cores")  # volta para a lista
    else:
        form = CorForm(initial={
            'id': cor.id,
            'nome': cor.nome,
            'tonalidade': cor.tonalidade,
            'ativa': cor.ativa,
        })
    return render(request, 'cadastra_cores.html', {'form': form, 'status': status})

@is_admin
def deleta_cores(request):
    cor = get_object_or_404(Cor, id=id)
    if request.method == 'POST':
        cor.delete()
        return redirect('exibe_cores')
    return render(request, 'confirma_exclusao.html', {'cor': cor})

@is_user
def cadastra_projetos(request):
    status = 0
    if request.method == "POST":
        form = ProjetoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            projeto = Projeto.objects.create(
                nome=cd["nome"],
                cliente=cd["cliente"],
                cor=cd["cor"],
                responsavel=cd["responsavel"],
                ativo=cd["ativo"],
            )
            # 🔹 marca a cor como ativa
            projeto.cor.ativa = True
            projeto.cor.save(update_fields=["ativa"])

            status = 1
            return redirect("exibe_projetos")
    else:
        form = ProjetoForm()

    return render(request, "cadastra_projetos.html", {"form": form, "status": status})

@is_user
def exibe_projetos(request):
    projetos = Projeto.objects.select_related("cor", "responsavel").all().order_by("nome")
    return render(request, "exibe_projetos.html", {"projetos": projetos})

@is_user
def edita_projetos(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    if request.method == "POST":
        form = ProjetoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # 🔹 se trocou de cor, libera a antiga e ativa a nova
            if projeto.cor != cd["cor"]:
                projeto.cor.ativa = False
                projeto.cor.save(update_fields=["ativa"])
                cd["cor"].ativa = True
                cd["cor"].save(update_fields=["ativa"])

            projeto.nome = cd["nome"]
            projeto.cliente = cd["cliente"]
            projeto.cor = cd["cor"]
            projeto.responsavel = cd["responsavel"]
            projeto.ativo = cd["ativo"]
            projeto.save()

            return redirect("exibe_projetos")
    else:
        form = ProjetoForm(initial={
            "id": projeto.id,
            "nome": projeto.nome,
            "cliente": projeto.cliente,
            "cor": projeto.cor,
            "responsavel": projeto.responsavel,
            "ativo": projeto.ativo,
        })
    return render(request, "cadastra_projetos.html", {"form": form})

@is_superuser
def deleta_projetos(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    projeto.delete()
    return redirect("exibe_projetos")

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

