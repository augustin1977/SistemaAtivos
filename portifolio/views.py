from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.http import FileResponse
from datetime import timedelta,date
from usuarios.autentica_usuario import *
from .models import *
from .forms import *
from .codigo_barras import *
from log.models import Log



@is_superuser
def cadastra_cores(request):
    status = 0
    if request.method == 'POST':
        form = CorForm(request.POST)
        if form.is_valid():
            cor=Cor.objects.create(
                nome=form.cleaned_data['nome'].capitalize(),
                tonalidade=form.cleaned_data['tonalidade'].upper(),
                ativa=form.cleaned_data.get('ativa', False),
            )
            status = 1
            Log.cadastramento(cor,Usuario.objects.get(id=request.session.get("usuario")),'cr')
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
            cd=form.cleaned_data
            lista_campos=["nome","tonalidade"]
            alteracao = False
            for campo in lista_campos:
                alterado=Log.foiAlterado(cor,campo,cd[campo],'cr',Usuario.objects.get(id=request.session.get("usuario")))
                if alterado:
                    setattr(cor, campo, cd[campo])
                alteracao |= alterado
            if alteracao:
                cor.save()
                messages.success(request, f"A cor '{cor.nome}' foi atualizada com sucesso!")
                status = 1
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
        Log.exclusao(cor,Usuario.objects.get(id=request.session.get("usuario")),'cr')
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
                Log.cadastramento(projeto,Usuario.objects.get(id=request.session.get("usuario")),'pj')   
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
            lista_campos=["nome","cliente","cor","responsavel"]
            # se trocou de cor, libera a antiga e ativa a nova
            if projeto.cor != cd["cor"]:
                projeto.cor.ativa = False
                projeto.cor.save(update_fields=["ativa"])
                cd["cor"].ativa = True
                cd["cor"].save(update_fields=["ativa"])
            alteracao = False
            for campo in lista_campos:
                alterado=Log.foiAlterado(projeto,campo,cd[campo],'pj',Usuario.objects.get(id=request.session.get("usuario")))
                if alterado:
                    setattr(projeto, campo, cd[campo])
                alteracao |= alterado
            if alteracao:
                try:
                    projeto.save()
                    messages.success(request, f"O projeto '{projeto.nome}' foi atualizado com sucesso!")
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
    amostras=Amostra.objects.filter(projeto=projeto, data_fim__isnull=True)
    for amostra in amostras:
        amostra.data_fim=hoje
        amostra.save(update_fields=["data_fim"])
        Log.finaliza(amostra,Usuario.objects.get(id=request.session.get("usuario")),'am')  
    Log.finaliza(projeto,Usuario.objects.get(id=request.session.get("usuario")),'pj')
    
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
        Log.reabre(projeto,Usuario.objects.get(id=request.session.get("usuario")),'pj')
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
        Log.reabre(projeto,Usuario.objects.get(id=request.session.get("usuario")),'pj')
        messages.success(request, f"O projeto '{projeto.nome}' foi reativado com sucesso.")
        return redirect("exibe_projetos_inativos")
@is_superuser
def deleta_projetos(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    projeto.cor.ativa = False
    projeto.cor.save(update_fields=["ativa"])
    projeto.delete()
    Log.exclusao(projeto,Usuario.objects.get(id=request.session.get("usuario")),'pj')
    messages.success(request, f"O projeto '{projeto.nome}' foi excluído com sucesso!")
    return redirect("exibe_projetos")

@is_user
def cadastra_amostras(request):
    status = 0
    if request.method == "POST":
        form = AmostraForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            amostra=Amostra.objects.create(
                nome=cd["nome"],
                projeto=cd["projeto"],
                data_recebimento=cd["data_recebimento"],
                prazo_dias=cd["prazo_dias"]
            )
            messages.success(request, "Amostra cadastrada com sucesso!")
            Log.cadastramento(amostra,Usuario.objects.get(id=request.session.get("usuario")),'am')
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
            lista_campos=["nome","projeto","data_recebimento","prazo_dias"]
            alteracao = False
            for campo in lista_campos:
                alterado=Log.foiAlterado(amostra,campo,cd[campo],'am',Usuario.objects.get(id=request.session.get("usuario")))
                if alterado:
                    setattr(amostra, campo, form.cleaned_data[campo])
                alteracao |= alterado
            if alteracao:
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
    Log.exclusao(amostra,Usuario.objects.get(id=request.session.get("usuario")),'am')
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
        Log.finaliza(amostra,Usuario.objects.get(id=request.session.get("usuario")),'am') 

        # Calcula prazo
        fim_previsto = amostra.data_recebimento + timedelta(days=amostra.prazo_dias)
        if amostra.data_fim <= fim_previsto:
            messages.success(request, f"A amostra '{amostra.nome}' foi finalizada dentro do prazo.")
        else:
            atraso = (amostra.data_fim - fim_previsto).days
            messages.warning(request, f"A amostra '{amostra.nome}' foi finalizada com {atraso} dia(s) de atraso.")

    return redirect("exibe_amostras")

@is_superuser
def reabre_amostra(request, id):
    amostra = get_object_or_404(Amostra, id=id)
    if not amostra.data_fim:
        messages.info(request, f"A amostra '{amostra.nome}' já está ativa.")
    else:
        amostra.data_fim = None
        amostra.save(update_fields=["data_fim"])
        Log.foiAlterado(amostra,"data_fim",None,'am',Usuario.objects.get(id=request.session.get("usuario")))
        Log.reabre(amostra,Usuario.objects.get(id=request.session.get("usuario")),'pj')
        messages.success(request, f"A amostra '{amostra.nome}' foi reaberta com sucesso.")
    return redirect("exibe_amostras_finalizadas")



@is_user
def cadastra_etiquetas(request):
    if request.method == "POST":
        form = EtiquetaForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            amostra = cd["amostra"]
            local_instalacao = cd["local_instalacao"]
            massa = cd["massa"]
            observacao = cd["observacao"]
            etiquetas_criadas = []

            codigo_humano = gerar_codigo_humano(amostra)
            codigo_numerico = gerar_codigo_numerico()

            etiqueta = Etiqueta.objects.create(
                amostra=amostra,
                local_instalacao=local_instalacao,
                massa=massa,
                codigo_humano=codigo_humano,
                codigo_numerico=codigo_numerico,
                observacao=observacao,
            )

            etiquetas_criadas.append(etiqueta)
        Log.cadastramento(etiqueta,Usuario.objects.get(id=request.session.get("usuario")),'et')  
        messages.success(
            request,
            f"{len(etiquetas_criadas)} etiqueta(s) criadas com sucesso!"
        )
        return redirect("exibe_etiquetas")

    else:
        form = EtiquetaForm()

    return render(request, "cadastra_etiquetas.html", {"form": form})
@is_user
def exibe_etiquetas(request):
    etiquetas = Etiqueta.objects.filter(amostra__data_fim__isnull=True).filter(amostra__projeto__ativo=True).select_related("amostra", "amostra__projeto", "amostra__projeto__cor").order_by("-codigo_numerico")
    
    
    return render(request, "exibe_etiquetas.html", {"etiquetas": etiquetas})
@is_user
def edita_etiquetas(request, id):
    etiqueta = get_object_or_404(Etiqueta, id=id)

    if request.method == "POST":
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            lista_campos=["amostra","local_instalacao","massa","observacao"]
            alteracao = False
            alterou_amostra = False
            for campo in lista_campos:
                alterado=Log.foiAlterado(etiqueta,campo,cd[campo],'et',Usuario.objects.get(id=request.session.get("usuario")))
                if alterado and campo == "amostra":
                    alterou_amostra = True
                if alterado:
                    setattr(etiqueta, campo, cd[campo])
                alteracao |= alterado
            if alterou_amostra:
                # Regenera os códigos se a amostra foi alterada
                # Gera novocodigo humano
                Log.foiAlterado(etiqueta,"codigo_humano",cd['codigo_humano'],'et',Usuario.objects.get(id=request.session.get("usuario")))
                codigo_humano = gerar_codigo_humano(cd['amostra'])
                setattr(etiqueta, "codigo_humano", codigo_humano)
                # Gera Novo codigo numerico
                codigo_numerico=gerar_codigo_numerico()
                cd["codigo_numerico"] = codigo_numerico
                Log.foiAlterado(etiqueta,"codigo_numerico",cd['codigo_numerico'],'et',Usuario.objects.get(id=request.session.get("usuario")))
                setattr(etiqueta, "codigo_numerico", cd["codigo_numerico"])
                
            if alteracao or alterou_amostra:
                etiqueta.save()
                messages.success(request, "Etiqueta atualizada com sucesso!")

            return redirect("exibe_etiquetas")
    else:
        form = EtiquetaForm(initial={
            "amostra": etiqueta.amostra,
            "local_instalacao": etiqueta.local_instalacao,
            "massa": etiqueta.massa,
            "observacao": etiqueta.observacao,
        })

    return render(request, "cadastra_etiquetas.html", {"form": form, "editando": True})

@is_user
def deleta_etiquetas(request, id):
    etiqueta = get_object_or_404(Etiqueta, id=id)
    etiqueta.delete()
    Log.exclusao(etiqueta,Usuario.objects.get(id=request.session.get("usuario")),'et')
    messages.success(request, "Etiqueta excluída com sucesso!")
    return redirect("exibe_etiquetas")
@is_user
def solicita_impressao_etiqueta(request, id):
    etiqueta = get_object_or_404(Etiqueta, id=id)
    
    if request.method == "POST":
        try:
            quantidade = int(request.POST.get("quantidade", 1))
        except ValueError:
            quantidade = 1

        if quantidade < 1:
            messages.error(request, "A quantidade deve ser pelo menos 1.")
            return redirect("solicita_impressao_etiqueta", id=id)

        # Redireciona para a view que gera o PDF
        return redirect(f"{reverse('imprime_etiquetas', args=[id])}?qtd={quantidade}")

    return render(request, "solicita_impressao_etiqueta.html", {"etiqueta": etiqueta})

@is_user
def imprime_etiquetas(request, id):
    etiqueta = get_object_or_404(Etiqueta, id=id)

    try:
        quantidade = int(request.GET.get("qtd", 1))
    except ValueError:
        quantidade = 1

    etiquetas = [etiqueta] * quantidade
    usuario_id=request.session.get('usuario')
    usuario=Usuario.objects.get(id=usuario_id)
     # Gera o PDF
    buffer = gerar_pdf_etiquetas(etiquetas, usuario)
    nome_pdf = f"etiqueta_{etiqueta.codigo_humano}_{quantidade}x.pdf"

    return FileResponse(buffer, as_attachment=True, filename=nome_pdf)

@is_user
def consulta_etiqueta(request):
    etiqueta = None
    query = request.GET.get("q", "").upper().strip()

    if query:
        etiqueta = Etiqueta.objects.filter(
            Q(codigo_humano__icontains=query) |
            Q(codigo_numerico__icontains=query) |
            Q(amostra__nome__icontains=query) |
            Q(amostra__projeto__nome__icontains=query)
        ).first()
        if not etiqueta:
            messages.error(request, "Etiqueta não encontrada. Verifique o código informado.")

    return render(request, "consulta_etiqueta.html", {"etiqueta": etiqueta, "query": query})


@is_user
def etiquetas_por_amostra(request, id_amostra):
    amostra = get_object_or_404(Amostra, id=id_amostra)
    etiquetas = Etiqueta.objects.filter(amostra=amostra)

    return render(request, "etiquetas_por_amostra.html", {
        "amostra": amostra,
        "etiquetas": etiquetas
    })

@is_user
def busca_etiquetas_por_local(request):
    locais = Local_instalacao.objects.filter(etiqueta__isnull=False).distinct().order_by('predio','piso','-sala','-armario','prateleira')
    etiquetas = None
    local_selecionado = None

    if request.method == "POST":
        local_id = request.POST.get("local_instalacao")
        if local_id:
            local_selecionado = get_object_or_404(Local_instalacao, id=local_id)
            etiquetas = Etiqueta.objects.filter(local_instalacao=local_selecionado) \
                                        .select_related("amostra", "amostra__projeto") \
                                        .order_by("amostra__projeto__nome", "amostra__nome")

    return render(request, "busca_etiquetas_por_local.html", {
        "locais": locais,
        "etiquetas": etiquetas,
        "local_selecionado": local_selecionado
    })

@is_user
def relatorio_prazo(request):
    projetos = Projeto.objects.filter(ativo=True).select_related('cor')
    dados = []

    for projeto in projetos:
        amostras = Amostra.objects.filter(projeto=projeto)
        total = amostras.count()

        if total == 0:
            dados.append({
                "projeto": projeto.nome,
                "projeto_id": projeto.id,
                "cor": getattr(projeto.cor, "css_color", "#ccc"),
                "total": 0,
                "no_prazo": 0,
                "fora_prazo": 0,
                "percentual": 0,
            })
            continue

        no_prazo = 0
        fora_prazo = 0

        for amostra in amostras:
            if amostra.data_recebimento:
                amostra.data_prevista = amostra.data_recebimento + timedelta(days=amostra.prazo_dias)
            else:
                amostra.data_prevista = None
            
            prazo_limite = amostra.data_recebimento + timedelta(days=amostra.prazo_dias)
            data_avaliacao = (amostra.data_fim) or datetime.today().date()

            if data_avaliacao <= prazo_limite:
                no_prazo += 1
            else:
                fora_prazo += 1

        percentual = round((no_prazo / total) * 100, 2) if total > 0 else 0

        dados.append({
            "projeto": projeto.nome,
            "projeto_id": projeto.id,
            "cor": getattr(projeto.cor, "css_color", "#ccc"),
            "total": total,
            "no_prazo": no_prazo,
            "fora_prazo": fora_prazo,
            "percentual": percentual,
        })
    dados.sort(key=lambda d: d["percentual"], reverse=True)
    return render(request, "relatorio_prazo.html", {"dados": dados})

@is_user
def amostras_por_projeto(request, projeto_id=None):
    projetos = Projeto.objects.filter(ativo=True).order_by("nome")
    projeto_selecionado = None
    amostras = []

    # Se vier via POST (seleção no formulário)
    if request.method == "POST":
        projeto_id = request.POST.get("projeto")

    # Se vier via GET (clicado no link do relatório)
    if projeto_id:
        projeto_selecionado = get_object_or_404(Projeto, id=projeto_id)
        amostras = (
            Amostra.objects.filter(projeto=projeto_selecionado)
            .select_related("projeto")
            .order_by("nome")
        )

        # Calcula a data prevista de fim para cada amostra
        for a in amostras:
            if a.data_recebimento:
                a.data_prevista = a.data_recebimento + timedelta(days=a.prazo_dias)
            else:
                a.data_prevista = None

    contexto = {
        "projetos": projetos,
        "projeto_selecionado": projeto_selecionado,
        "amostras": amostras,
        "today": date.today(),
    }
    
    return render(request, "amostras_por_projeto.html", contexto)