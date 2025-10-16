from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
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
            #cor.ativa = form.cleaned_data.get('ativa', False)
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
def deleta_cores(request,id):
    cor = get_object_or_404(Cor, id=id)
    if request.method == 'POST':
        if Projeto.objects.filter(cor=cor).exists():
            messages.error(request,f"A cor '{cor.nome}' não pode ser excluída, pois está associada a um ou mais projetos.")
            return redirect('exibe_cores')
        cor.delete()
        messages.success(request, f"A cor '{cor.nome}' foi excluída com sucesso!")
        return redirect('exibe_cores')
    return render(request, 'confirma_exclusao.html', {'cor': cor})

@is_user
def cadastra_projetos(request):
    status = 0
    if request.method == "POST":
        form = ProjetoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                projeto = Projeto.objects.create(
                nome=cd["nome"],
                cliente=cd["cliente"],
                cor=cd["cor"],
                responsavel=cd["responsavel"],
                ativo=True,            )
                # 🔹 marca a cor como ativa
                projeto.cor.ativa = True
                projeto.cor.save(update_fields=["ativa"])

                status = 1
                return redirect("exibe_projetos")
            except IntegrityError:
                form.add_error("nome", "Já existe um projeto com este nome.")
    else:
        form = ProjetoForm()

    return render(request, "cadastra_projetos.html", {"form": form, "status": status})

@is_user
def exibe_projetos(request):
    projetos = Projeto.objects.filter(ativo=True).select_related("cor", "responsavel").order_by("-data_criacao")
    return render(request, "exibe_projetos.html", {"projetos": projetos, "mostrando_inativos": False})

@is_user
def exibe_projetos_inativos(request):
    projetos = Projeto.objects.filter(ativo=False).select_related("cor", "responsavel").order_by("-data_criacao")
    return render(request, "exibe_projetos.html", {"projetos": projetos,"mostrando_inativos": True,})

@is_user
def edita_projetos(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    if request.method == "POST":
        form = ProjetoForm(request.POST, cor_atual=projeto.cor)
        if form.is_valid():
            cd = form.cleaned_data

            # se trocou de cor, libera a antiga e ativa a nova
            if projeto.cor != cd["cor"]:
                projeto.cor.ativa = False
                projeto.cor.save(update_fields=["ativa"])
                cd["cor"].ativa = True
                cd["cor"].save(update_fields=["ativa"])

            projeto.nome = cd["nome"].strip()
            projeto.cliente = cd["cliente"].strip()
            projeto.cor = cd["cor"]
            projeto.responsavel = cd["responsavel"]
            #projeto.ativo = cd.get("ativo", False)

            try:
                projeto.save()
                return redirect("exibe_projetos")
            except IntegrityError:
                form.add_error("nome", "Já existe um projeto com este nome.")
    else:
        form = ProjetoForm(
            initial={
                "id": projeto.id,
                "nome": projeto.nome,
                "cliente": projeto.cliente,
                "cor": projeto.cor,                # pré-selecionada
                "responsavel": projeto.responsavel,
                "ativo": projeto.ativo,
            },
            cor_atual=projeto.cor,                  # inclui a cor atual no queryset
        )
    return render(request, "cadastra_projetos.html", {
        "form": form,
        "status": 0,
        "editing": True,
        "projeto": projeto,
    })
    
@is_user
def desativa_projetos(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    projeto.ativo = False
    projeto.cor.ativa = False
    projeto.cor.save(update_fields=["ativa"])
    projeto.save(update_fields=["ativo"])
    hoje = timezone.now().date()
    Amostra.objects.filter(projeto=projeto, data_fim__isnull=True).update(data_fim=hoje)
    messages.success(request, f"Projeto '{projeto.nome}' foi encerrado com sucesso e suas amostras foram finalizadas.")
    return redirect("exibe_projetos")

@is_user
def ativa_projetos(request, id):
   
    projeto = get_object_or_404(Projeto, id=id)
    
    # verifica se a cor do projeto está em uso por outro projeto ativo
    cor_em_uso = Projeto.objects.filter(ativo=True, cor=projeto.cor).exclude(id=projeto.id).exists()
    
    if request.method == "POST":
        nova_cor_id = request.POST.get("cor_id")
        if nova_cor_id:
            nova_cor = get_object_or_404(Cor, id=nova_cor_id)
            projeto.cor = nova_cor
        projeto.ativo = True
        projeto.cor.ativa = True
        projeto.cor.save(update_fields=["ativa"])
        projeto.save(update_fields=["ativo", "cor"])
        messages.success(request, f"O projeto '{projeto.nome}' foi reaberto com sucesso.")
        return redirect("exibe_projetos_inativos")
    
    if cor_em_uso:
        cores_disponiveis = Cor.objects.filter(ativa=False).exclude(id=projeto.cor.id)
        return render(request, "reativa_projeto.html", {
            "projeto": projeto,
            "cores_disponiveis": cores_disponiveis,
        })
    else:
        projeto.ativo = True
        projeto.cor.ativa = True
        projeto.cor.save(update_fields=["ativa"])
        projeto.save(update_fields=["ativo"])
        messages.success(request, f"O projeto '{projeto.nome}' foi reativado com sucesso.")
        return redirect("exibe_projetos_inativos")
@is_admin
def deleta_projetos(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    projeto.cor.ativa = False
    projeto.cor.save(update_fields=["ativa"])
    projeto.delete()
    return redirect("exibe_projetos")

@is_user
def cadastra_amostras(request):
    status = 0
    if request.method == "POST":
        form = AmostraForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Amostra.objects.create(
                nome=cd["nome"],
                projeto=cd["projeto"],
                data_recebimento=cd["data_recebimento"],
                prazo_dias=cd["prazo_dias"]
            )
            messages.success(request, "Amostra cadastrada com sucesso!")
            return redirect("exibe_amostras")
    else:
        form = AmostraForm()
    return render(request, "cadastra_amostras.html", {"form": form, "status": status})
@is_user
def exibe_amostras(request):
    amostras = Amostra.objects.filter(
        projeto__ativo=True,
        data_fim__isnull=True
    ).select_related("projeto").order_by("-data_recebimento")

    return render(request, "exibe_amostras.html", {
        "amostras": amostras,
        "mostrando_finalizadas": False
    })
@is_user
def exibe_amostras_finalizadas(request):
    amostras = Amostra.objects.filter(
        models.Q(data_fim__isnull=False) | models.Q(projeto__ativo=False)
    ).select_related("projeto").order_by("-data_fim", "-data_recebimento")

    return render(request, "exibe_amostras.html", {
        "amostras": amostras,
        "mostrando_finalizadas": True
    })
    
@is_user
def edita_amostras(request, id):
    amostra = get_object_or_404(Amostra, id=id)
    if request.method == "POST":
        form = AmostraForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            amostra.nome = cd["nome"]
            amostra.projeto = cd["projeto"]
            amostra.data_recebimento = cd["data_recebimento"]
            amostra.prazo_dias = cd["prazo_dias"]
            amostra.save()
            messages.success(request, "Amostra atualizada com sucesso!")
            return redirect("exibe_amostras")
    else:
        form = AmostraForm(initial={
            "id": amostra.id,
            "nome": amostra.nome,
            "projeto": amostra.projeto,
            "data_recebimento": amostra.data_recebimento,
            "data_fim": amostra.data_fim,
            "prazo_dias": amostra.prazo_dias
        })
    return render(request, "cadastra_amostras.html", {"form": form})
@is_user
def deleta_amostras(request, id):
    amostra = get_object_or_404(Amostra, id=id)
    amostra.delete()
    messages.warning(request, f"Amostra '{amostra.nome}' foi removida.")
    return redirect("exibe_amostras")
@is_user
def finaliza_amostra(request, id):
    amostra = get_object_or_404(Amostra, id=id)

    if amostra.data_fim:
        messages.warning(request, f"A amostra '{amostra.nome}' já foi finalizada em {amostra.data_fim}.")
    else:
        amostra.data_fim = timezone.now().date()
        amostra.save(update_fields=["data_fim"])

        # Calcula prazo
        fim_previsto = amostra.data_recebimento + timedelta(days=amostra.prazo_dias)
        if amostra.data_fim <= fim_previsto:
            messages.success(request, f"A amostra '{amostra.nome}' foi finalizada dentro do prazo.")
        else:
            atraso = (amostra.data_fim - fim_previsto).days
            messages.warning(request, f"A amostra '{amostra.nome}' foi finalizada com {atraso} dia(s) de atraso.")

    return redirect("exibe_amostras")
@is_user
def reabre_amostra(request, id):
    amostra = get_object_or_404(Amostra, id=id)
    if not amostra.data_fim:
        messages.info(request, f"A amostra '{amostra.nome}' já está ativa.")
    else:
        amostra.data_fim = None
        amostra.save(update_fields=["data_fim"])
        messages.success(request, f"A amostra '{amostra.nome}' foi reaberta com sucesso.")
    return redirect("exibe_amostras_finalizadas")


@is_user
def cadastra_etiquetas(request):
    return render(request, "em_construcao.html")
@is_user
def exibe_etiquetas(request):
    return render(request, "em_construcao.html")
@is_user
def edita_etiquetas(request):
    return render(request, "em_construcao.html")
@is_user
def deleta_etiquetas(request):
    return render(request, "em_construcao.html")
@is_user
def imprime_etiquetas(request):
    return render(request, "em_construcao.html")

