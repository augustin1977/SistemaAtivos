# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from django.contrib.staticfiles.views import serve
from django.http import HttpResponse
from .models import *
from notas.models import *
from django.shortcuts import redirect
from cadastro_equipamentos import settings
from django.http import HttpResponse, Http404
from os import path
from cadastro_equipamentos.settings import BASE_DIR, MEDIA_ROOT, TIME_ZONE
import os, csv
from log.models import Log
from .forms import *
import equipamentos.funcoesAuxiliares as funcoesAuxiliares
from equipamentos.calcula_dados_sistema import *
from django.db.models import Q
import json
from datetime import datetime
import dados_ambiente
from usuarios.autentica_usuario import *

def home(request):
    """verify if has already a user logged in, if yes render home.html else redirect to login page

    Args:
        request (usuario): verifiy if there is a user loged in.

    Returns:
        HTML page: render home.thml
    """
    if not request.session.get("usuario"):
        return redirect("/auth/login/?status=2")
    # cria a view do login do usuário
    status = str(request.GET.get("status"))
    return render(request, "home.html", {"status": status})

@is_user
def menuEquipoamento(request):
    """Render initial page of system

    Args:
        request (request): request username login

    Returns:
        _type_: render equipamento.html
    """

    # cria a view do login do usuário
    status = str(request.GET.get("status"))
    return render(request, "equipamentos.html", {"status": status})

@is_user
def lista_equipamentos(request):
    # print(f"{usu.nome} acessou Lista Equipamentos")
    equipamentos = Equipamento.objects.filter(ativo=True)
    return render(request, "exibirEquipamentos.html", {"equipamentos": equipamentos})


def get_equipamentos(request):
    termo_busca = request.GET.get("nome_equipamento", "")
    equipamentos = []

    if len(termo_busca) > 2:
        q1 = Q(nome_equipamento__icontains=termo_busca)
        q2 = Q(codigo__icontains=termo_busca)
        q3 = Q(fabricante__nome_fabricante__icontains=termo_busca)
        q4 = Q(patrimonio=termo_busca)
        q5 = Q(modelo__icontains=termo_busca)
        q9 = Q(ativo=True)

        filtro = (q1 | q2 | q3 | q4 | q5) & q9
        equipamentos = Equipamento.objects.filter(filtro)
    else:
        equipamentos = Equipamento.objects.filter(ativo=True)
    equipamentos_json = json.dumps(
        [equipamento.to_dic() for equipamento in equipamentos], ensure_ascii=False
    )
    return HttpResponse(equipamentos_json, content_type="application/json")

@is_user
def exibirDetalheEquipamento(request):
    """Renderizar pagiina com detalhes do equipamento"""
    id = str(request.GET.get("id"))
    usuario = Usuario.objects.get(id=request.session.get("usuario"))
    equipamento = Equipamento.objects.get(id=id, ativo=True)
    equipamento.data_compra= funcoesAuxiliares.formatar_data_por_extenso(equipamento.data_compra)
    equipamento.data_ultima_calibracao= funcoesAuxiliares.formatar_data_por_extenso(equipamento.data_ultima_calibracao)
    materiais = Material_consumo.objects.filter(equipamento__id=id)
    arquivos = Media.objects.filter(equipamento__id=id)
    permissoes = Autorizacao_equipamento.objects.filter(equipamento=equipamento)
    # log=Log(transacao='eq',movimento='lt',usuario=usuario,equipamento=equipamento,alteracao=f'{usuario} listou detalhe equipamento: {equipamento}')
    # log.save()
    return render(request,
        "exibirDetalheEquipamento.html",
        {
            "equipamento": equipamento,
            "materiais": materiais,
            "media": arquivos,
            "confirmarexluir": "0",
            "permissoes":permissoes
        },
    )

@is_user
def editarEquipamento(request):
    usuario = Usuario.objects.get(id=request.session.get("usuario"))
    if request.method == "GET":
        equipamento = request.GET.get("equipamento")
        dados = Equipamento.objects.get(id=equipamento, ativo=True)
        dados_paraformulario = dados.dados_para_form()
        form = equipamentoEditarForm(initial=dados_paraformulario)
        return render(request, "editarEquipamento.html", {"form": form})
    elif request.method == "POST":
        form  = equipamentoEditarForm(request.POST)
        
        if form.is_valid():
            e = Equipamento.objects.get(id=form.cleaned_data["id"], ativo=True)
            listaCampos = [
                "nome_equipamento",
                "modelo",
                "fabricante",
                "local",
                "tipo_equipamento",
                "data_compra",
                "data_ultima_calibracao",
                "patrimonio",
                "codigo",
                "custo_aquisição",
                "responsavel",
                "potencia_eletrica",
                "nacionalidade",
                "data_ultima_atualizacao",
                "tensao_eletrica",
                "projeto_compra",
                "especificacao",
                "outros_dados",
            ]
            alteracao = False
            for campo in listaCampos:
                alterado = Log.foiAlterado(
                    transacao="eq",
                    objeto=e,
                    atributo=campo,
                    equipamento=e,
                    valor=form.cleaned_data[campo],
                    usuario=usuario,
                )
                if alterado:
                    setattr(e, campo, form.cleaned_data[campo])
                alteracao |= alterado
            if alteracao:
                e.save()
                # print(e.data_cadastro)
            # bloco comentado pois os materiais não foram implementados

            # lista_materiais=Material_consumo.objects.filter(equipamento__id=details.cleaned_data['id'])
            # for material in details.cleaned_data['material_consumo']:
            #     if material not in lista_materiais:
            #         log=Log(transacao='mc',usuario=usuario,equipamento=e,alteracao=f'O usuario {usuario} cadastrou o material {material} no equipamento {e}')
            #         log.save()
            #         e.material_consumo.add(material)
            # for material in lista_materiais:
            #     if material not in details.cleaned_data['material_consumo']:
            #         e.material_consumo.remove(material)
            #         log=Log(transacao='mc',movimento='dl',usuario=usuario,equipmento=e,alteracao=f'o usuario {usuario} excluiu o material {material} do equipamento {e}')
            #         log.save()
            mecanica = Disciplina.objects.get(disciplina="Mecânica")
            geral = Disciplina.objects.get(disciplina="Geral")
            outros = Disciplina.objects.get(disciplina="Outros")
            melhoria=Disciplina.objects.get(disciplina="Melhoria")
            movimentacao=Disciplina.objects.get(disciplina="Movimentação")
            filtro1 = Q(disciplina=mecanica)
            filtro2 = Q(disciplina=geral)
            filtro3 = Q(disciplina=outros)
            filtro4 = Q(disciplina=melhoria)
            filtro5 = Q(disciplina=movimentacao)
            modos = Modo_Falha.objects.filter(filtro1 | filtro2 | filtro3 | filtro4 | filtro5)
            filtroequipamento= Q(equipamento=e) 
            for modo in modos:
                filtromodo= Q(modo_falha=modo) 
                if not Modo_falha_equipamento.objects.filter(filtroequipamento & filtromodo):
                    m = Modo_falha_equipamento(equipamento=e, modo_falha=modo)
                    m.save()
            if e.potencia_eletrica or e.tensao_eletrica:
                modos = Modo_Falha.objects.filter(
                    disciplina=Disciplina.objects.get(disciplina="Elétrica")
                )
                for modo in modos:
                    filtromodo= Q(modo_falha=modo) 
                    if not Modo_falha_equipamento.objects.filter(filtroequipamento & filtromodo):
                        m = Modo_falha_equipamento(equipamento=e, modo_falha=modo)
                        m.save()   
            equipamentos = Equipamento.objects.filter(ativo=True)
            return render(request, "exibirEquipamentos.html", {"equipamentos": equipamentos})
        else:
            # Renderizar o formulário novamente com os erros
            equipamento_id = request.POST.get("id")
            equipamento = Equipamento.objects.get(id=equipamento_id, ativo=True)
            return render(request, "editarEquipamento.html", {"form": form, "equipamento": equipamento})

@is_superuser
def cadastrarEquipamento(request):

    usuario = Usuario.objects.get(id=request.session.get("usuario"))


   

    if request.method == "GET":
        form = equipamentoCadastrarForm(
            initial={"usuario": request.session.get("usuario")}
        )

        return render(request, "cadastrarEquipamento.html", {"form": form, "status": 0})
    else:
        details = equipamentoCadastrarForm(request.POST)

        if details.is_valid():
            nome_equipamento = details.cleaned_data["nome_equipamento"]
            modelo = details.cleaned_data["modelo"]
            fabricante = details.cleaned_data["fabricante"]
            local = details.cleaned_data["local"]
            tipo_equipamento = details.cleaned_data["tipo_equipamento"]
            data_compra = details.cleaned_data["data_compra"]
            data_ultima_calibracao = details.cleaned_data["data_ultima_calibracao"]
            data_cadastro = details.cleaned_data["data_cadastro"]
            patrimonio = details.cleaned_data["patrimonio"]
            # material_consumo=details.cleaned_data['material_consumo']
            material_consumo = []
            usuario = details.cleaned_data["usuario"]
            codigo = details.cleaned_data["codigo"]
            custo_aquisição = details.cleaned_data["custo_aquisição"]
            responsavel = details.cleaned_data["responsavel"]
            potencia_eletrica = details.cleaned_data["potencia_eletrica"]
            nacionalidade = details.cleaned_data["nacionalidade"]
            data_ultima_atualizacao = details.cleaned_data["data_ultima_atualizacao"]
            tensao_eletrica = details.cleaned_data["tensao_eletrica"]
            projeto_compra = details.cleaned_data["projeto_compra"]
            especificacao = details.cleaned_data["especificacao"]
            outros_dados = details.cleaned_data["outros_dados"]

            e = Equipamento(
                nome_equipamento=nome_equipamento,
                modelo=modelo,
                fabricante=fabricante,
                local=local,
                tipo_equipamento=tipo_equipamento,
                data_cadastro=data_cadastro,
                data_compra=data_compra,
                data_ultima_calibracao=data_ultima_calibracao,
                patrimonio=patrimonio,
                usuario=Usuario.objects.get(id=usuario),
                codigo=codigo,
                responsavel=responsavel,
                potencia_eletrica=potencia_eletrica,
                nacionalidade=nacionalidade,
                data_ultima_atualizacao=data_ultima_atualizacao,
                tensao_eletrica=tensao_eletrica,
                projeto_compra=projeto_compra,
                especificacao=especificacao,
                outros_dados=outros_dados,
                custo_aquisição=custo_aquisição,
                ativo=True,
            )
            e.save()
            mecanica = Disciplina.objects.get(disciplina="Mecânica")
            geral = Disciplina.objects.get(disciplina="Geral")
            outros = Disciplina.objects.get(disciplina="Outros")
            melhoria=Disciplina.objects.get(disciplina="Melhoria")
            movimentacao=Disciplina.objects.get(disciplina="Movimentação")

            filtro1 = Q(disciplina=mecanica)
            filtro2 = Q(disciplina=geral)
            filtro3 = Q(disciplina=outros)
            filtro4 = Q(disciplina=melhoria)
            filtro5 = Q(disciplina=movimentacao)
            modos = Modo_Falha.objects.filter(filtro1 | filtro2 | filtro3 | filtro4 | filtro5)
            for modo in modos:
                m = Modo_falha_equipamento(equipamento=e, modo_falha=modo)
                m.save()
            if e.potencia_eletrica or e.tensao_eletrica:
                modos = Modo_Falha.objects.filter(
                    disciplina=Disciplina.objects.get(disciplina="Elétrica")
                )
                for modo in modos:
                    m = Modo_falha_equipamento(equipamento=e, modo_falha=modo)
                    m.save()

            usuario = Usuario.objects.get(id=request.session.get("usuario"))
            Log.cadastramento(objeto=e, transacao="eq", usuario=usuario, equipamento=e)
            # Cadastrando modos de falha Equipamento

            for material in material_consumo:
                e.material_consumo.add(material)
                log = Log(
                    transacao="mc",
                    movimento="cd",
                    usuario=usuario,
                    equipmento=e,
                    alteracao=f"o usuario {usuario} cadastrou o {material} no equipamento {e} id={e.id}",
                )
                log.save()

            form = equipamentoCadastrarForm(
                initial={"usuario": request.session.get("usuario")}
            )
            return render(
                request,
                "cadastrarEquipamento.html",
                {
                    "form": form,
                    "status": 1,
                    "equipamento": nome_equipamento + " - " + codigo,
                },
            )
        else:
            return render(request, "cadastrarEquipamento.html", {"form": details})

@is_superuser
def excluirEquipamento(request):

    id = str(request.GET.get("id"))
    equipamento = Equipamento.objects.get(id=id, ativo=True)
    usuario = Usuario.objects.get(id=request.session.get("usuario"))
    if request.GET.get("excluir") == "2":
        equipamento.ativo = False
        local = Local_instalacao.objects.get(laboratorio="Descarte")
        equipamento.local = local
        equipamento.save()
        Log.exclusao(
            objeto=equipamento, transacao="eq", usuario=usuario, equipamento=equipamento
        )
        return redirect("/equipamentos/listarEquipamentos")

    materiais = Material_consumo.objects.filter(equipamento__id=id)
    arquivos = Media.objects.filter(equipamento__id=id)
    # print('excluir',request.GET.get('excluir'))
    return render(
        request,
        "exibirDetalheEquipamento.html",
        {
            "equipamento": equipamento,
            "materiais": materiais,
            "media": arquivos,
            "confirmarexluir": request.GET.get("excluir"),
        },
    )

@is_user
def listarFornecedores(request):
    # print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Lista Fornecedores")
    fornecedores = Fabricante.objects.all()
    return render(request, "listarFornecedores.html", {"fornecedores": fornecedores})

@is_user
def exibirDetalheFornecedor(request):
    id = str(request.GET.get("id"))
    fornecedor = Fabricante.objects.get(id=id)
    if fornecedor.endereco_fabricante == None:
        fornecedor.endereco_fabricante = ""
    if (
        fornecedor.nome_contato_fabricante == None
        or fornecedor.nome_contato_fabricante == "None"
    ):
        fornecedor.nome_contato_fabricante = ""
    if fornecedor.telefone_contato == None:
        fornecedor.telefone_contato = ""
    if fornecedor.email_contato_fabricante == None:
        fornecedor.email_contato_fabricante = ""
    if fornecedor.site_Fabricante == None:
        fornecedor.site_Fabricante = ""
    if fornecedor.dados_adicionais == None:
        fornecedor.dados_adicionais = ""
    return render(request, "exibirDetalhefornecedor.html", {"fornecedor": fornecedor})

@is_user
def cadastrarFornecedor(request):
    usuario = Usuario.objects.get(id=request.session.get("usuario"))
    if request.method == "GET":
        return render(request, "cadastrarFornecedor.html")
    else:
        # captura dados
        post_nome_fabricante = request.POST.get("nome_fabricante")
        post_endereco_fabricante = request.POST.get("endereco_fabricante")
        post_nome_contato_fabricante = request.POST.get("nome_contato_fabricante")
        post_telefone_contato = request.POST.get("telefone_contato")
        post_email_contato_fabricante = request.POST.get("email_contato_fabricante")
        post_site_Fabricante = request.POST.get("site_Fabricante")
        post_dados_adicionais = request.POST.get("dados_adicionais")
        # verifica campo vazio e coloca None
        if post_endereco_fabricante == "":
            post_endereco_fabricante = None
        if post_nome_contato_fabricante == "":
            post_nome_contato_fabricante = None
        if post_telefone_contato == "":
            post_telefone_contato = None
        if post_email_contato_fabricante == "":
            post_email_contato_fabricante = None
        if post_site_Fabricante == "":
            post_site_Fabricante = None
        if post_dados_adicionais == "":
            post_dados_adicionais = None
        # busca por dados repetidos no banco de dados
        nome = Fabricante.objects.filter(nome_fabricante=post_nome_fabricante).first()
        site = Fabricante.objects.filter(site_Fabricante=post_site_Fabricante).first()
        email = Fabricante.objects.filter(
            email_contato_fabricante=post_email_contato_fabricante
        ).first()
        # verifica se forncedor ja existe
        if nome and site and email:
            return render(
                request, "cadastrarFornecedor.html", {"status": 1}
            )  # fornecedor ja cadastrado
        # verifica se estão preenchidos campos obrigatórios
        if not post_nome_fabricante:
            return render(
                request, "cadastrarFornecedor.html", {"status": 2}
            )  # campos obrigatórios não preenchidos
        # verfica digitação do email e do telefone
        regex_email = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        # if post_email_contato_fabricante:
        #    if not (re.search(regex_email, post_email_contato_fabricante)):
        #        return render(request, "cadastrarFornecedor.html", {'status':3}) # email com digitação incorreta
        fabricante = Fabricante(
            nome_fabricante=post_nome_fabricante,
            endereco_fabricante=post_endereco_fabricante,
            nome_contato_fabricante=post_nome_contato_fabricante,
            telefone_contato=post_telefone_contato,
            email_contato_fabricante=post_email_contato_fabricante,
            site_Fabricante=post_site_Fabricante,
            dados_adicionais=post_dados_adicionais,
        )
        fabricante.save()
        Log.cadastramento(usuario=usuario, transacao="fn", objeto=fabricante)
        return render(request, "cadastrarFornecedor.html", {"status": 0})

@is_user
def editarFornecedor(request):
    id = request.GET.get("id")
    if id:
        if request.method == "GET":
            fornecedor = Fabricante.objects.get(id=id)
            return render(request, "editarFornecedor.html", {"fornecedor": fornecedor})
    if request.method == "POST":
        post_id = request.POST.get("id")
        post_nome_fabricante = request.POST.get("nome_fabricante")
        post_endereco_fabricante = request.POST.get("endereco_fabricante")
        post_nome_contato_fabricante = request.POST.get("nome_contato_fabricante")
        post_telefone_contato = request.POST.get("Telefone_contato_fabricante")
        post_email_contato_fabricante = request.POST.get("email_contato_fabricante")
        post_site_Fabricante = request.POST.get("site_Fabricante")
        post_dados_adicionais = request.POST.get("dados_adicionais")
        # verifica campo vazio e coloca None
        if post_endereco_fabricante == "" or post_endereco_fabricante == "None":
            post_endereco_fabricante = None
        if post_nome_contato_fabricante == "" or post_nome_contato_fabricante == "None":
            post_telefone_contato = None
        if post_telefone_contato == "" or post_telefone_contato == "None":
            post_telefone_contato = None
        if (
            post_email_contato_fabricante == ""
            or post_email_contato_fabricante == "None"
        ):
            post_email_contato_fabricante = None
        if post_site_Fabricante == "" or post_site_Fabricante == "None ":
            post_site_Fabricante = None
        if post_dados_adicionais == "" or post_dados_adicionais == "None":
            post_dados_adicionais = None
        fornecedor = Fabricante.objects.get(id=post_id)
        # busca por dados repetidos no banco de dados
        nome = Fabricante.objects.filter(nome_fabricante=post_nome_fabricante).first()
        site = Fabricante.objects.filter(site_Fabricante=post_site_Fabricante).first()
        email = Fabricante.objects.filter(
            email_contato_fabricante=post_email_contato_fabricante
        ).first()
        ##print(post_nome_fabricante)
        # verifica se forncedor ja existe
        if (nome and nome.id != fornecedor.id) and site and email:
            return render(
                request,
                "editarFornecedor.html",
                {"fornecedor": fornecedor, "status": 1},
            )  # fornecedor ja cadastrado
        # verifica se estão preenchidos campos obrigatórios
        if not post_nome_fabricante:
            return render(
                request,
                "editarFornecedor.html",
                {"fornecedor": fornecedor, "status": 2},
            )  # campos obrigatórios não preenchidos
        # verfica digitação do email e do telefone
        regex_email = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        # if post_email_contato_fabricante:
        # if not (re.search(regex_email, post_email_contato_fabricante)):
        # return render(request, "editarFornecedor.html", {'fornecedor':fornecedor,'status':3}) # email com digitação incorreta
        usuario = Usuario.objects.get(id=request.session.get("usuario"))
        if Log.foiAlterado(
            objeto=fornecedor,
            atributo="nome_fabricante",
            valor=post_nome_fabricante,
            usuario=usuario,
            transacao="fn",
        ):
            fornecedor.nome_fabricante = post_nome_fabricante
        if Log.foiAlterado(
            objeto=fornecedor,
            atributo="endereco_fabricante",
            valor=post_endereco_fabricante,
            usuario=usuario,
            transacao="fn",
        ):
            fornecedor.endereco_fabricante = post_endereco_fabricante
        if Log.foiAlterado(
            objeto=fornecedor,
            atributo="nome_contato_fabricante",
            valor=post_nome_contato_fabricante,
            usuario=usuario,
            transacao="fn",
        ):
            fornecedor.nome_contato_fabricante = post_nome_contato_fabricante
        if Log.foiAlterado(
            objeto=fornecedor,
            atributo="telefone_contato",
            valor=post_telefone_contato,
            usuario=usuario,
            transacao="fn",
        ):
            fornecedor.telefone_contato = post_telefone_contato
        if Log.foiAlterado(
            objeto=fornecedor,
            atributo="email_contato_fabricante",
            valor=post_email_contato_fabricante,
            usuario=usuario,
            transacao="fn",
        ):
            fornecedor.email_contato_fabricante = post_email_contato_fabricante
        if Log.foiAlterado(
            objeto=fornecedor,
            atributo="site_Fabricante",
            valor=post_site_Fabricante,
            usuario=usuario,
            transacao="fn",
        ):
            fornecedor.site_Fabricante = post_site_Fabricante
        if Log.foiAlterado(
            objeto=fornecedor,
            atributo="dados_adicionais",
            valor=post_dados_adicionais,
            usuario=usuario,
            transacao="fn",
        ):
            fornecedor.dados_adicionais = post_dados_adicionais
        fornecedor.save()
        return redirect("/equipamentos/listarFornecedores/?status=10")

    return redirect("/equipamentos/listarFornecedores/")

@is_user
def cadastrarLocal(request):
    # print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou cadastro local")
    if request.method == "GET":
        form = localFormCadastro
        return render(request, "cadastrarLocal.html", {"form": form, "status": 0})
    else:
        details = localFormCadastro(request.POST)
        if details.is_valid():
            # print(details)
            details.save()
            form = localFormCadastro
            usuario = Usuario.objects.get(id=request.session.get("usuario"))

            local = Local_instalacao.objects.get(
                laboratorio=details.cleaned_data["laboratorio"],
                sala=details.cleaned_data["sala"],
                predio=details.cleaned_data["predio"],
                piso=details.cleaned_data["piso"],
                apelido_local=details.cleaned_data["apelido_local"],
                armario=details.cleaned_data["armario"],
                prateleira=details.cleaned_data["prateleira"],
            )
            Log.cadastramento(usuario=usuario, transacao="li", objeto=local)
            return render(request, "cadastrarLocal.html", {"form": form, "status": 1})
        else:
            # print('invalido')
            return render(request, "cadastrarLocal.html", {"form": details})

@is_user
def listarLocais(request):
    if request.method == "GET":
        form = Local_instalacao.objects.all()
        return render(request, "listarLocais.html", {"form": form, "status": 0})

@is_user
def editarLocal(request):
    usuario = Usuario.objects.get(id=request.session.get("usuario"))
    if request.method == "GET":
        dados = Local_instalacao.objects.get(id=request.GET.get("id")).dados_para_form()
        form = localFormEditar(initial=dados)
        return render(
            request,
            "editarLocal.html",
            {"form": form, "id": request.GET.get("id"), "status": 0},
        )
    else:
        form = Local_instalacao.objects.all()
        details = localFormEditar(request.POST)
        if details.is_valid():
            e = Local_instalacao.objects.get(id=details.cleaned_data["id"])
            listaCampos = [
                "laboratorio",
                "predio",
                "piso",
                "sala",
                "armario",
                "prateleira",
                "apelido_local",
            ]
            alteracao = False
            for campo in listaCampos:
                alterado = Log.foiAlterado(
                    transacao="li",
                    objeto=e,
                    atributo=campo,
                    valor=details.cleaned_data[campo],
                    usuario=usuario,
                )
                if alterado:
                    setattr(e, campo, details.cleaned_data[campo])
                alteracao |= alterado
            if alteracao:
                e.save()
            return render(request, "listarLocais.html", {"form": form, "status": 1})
        else:
            return render(request, "listarLocais.html", {"form": form, "status": 2})

@is_admin
def cadastrarTipo(request):
    usuario = Usuario.objects.get(id=request.session.get("usuario"))
    if request.method == "GET":
        form = cadastraTipo_equipamento
        return render(request, "cadastrarTipo.html", {"form": form, "status": 0})
    else:
        details = cadastraTipo_equipamento(request.POST)
        if details.is_valid():
            # print('valido')

            tipo = Tipo_equipamento(
                nome_tipo=details.cleaned_data["nome"],
                sigla=details.cleaned_data["sigla"],
                descricao_tipo=details.cleaned_data["descricao"],
            )
            tipo.save()
            Log.cadastramento(usuario=usuario, transacao="te", objeto=tipo)
            form = cadastraTipo_equipamento

            return render(request, "cadastrarTipo.html", {"form": form, "status": 1})
        else:
            # print('invalido')
            return render(request, "cadastrarTipo.html", {"form": details})

@is_admin
def editarTipo(request):
    usuario = Usuario.objects.get(id=request.session.get("usuario"))
    if request.method == "GET":
        dados = Tipo_equipamento.objects.get(id=request.GET.get("id")).dados_para_form()
        # print(dados)
        form = TipoEquipamentoForm(initial=dados)
        return render(
            request,
            "editarTipo.html",
            {"form": form, "id": request.GET.get("id"), "status": 0},
        )
    else:
        details = TipoEquipamentoForm(request.POST)
        if details.is_valid():
            # print('valido')
            tipo = Tipo_equipamento.objects.get(id=details.cleaned_data["id"])
            outros = Tipo_equipamento.objects.get(nome_tipo="Outros")
            if tipo == outros:
                return redirect("/equipamentos/listarTipo/?status=50")
            listaCampos = ["nome_tipo", "descricao_tipo"]
            alteracao = False
            for campo in listaCampos:
                alterado = Log.foiAlterado(
                    transacao="te",
                    objeto=tipo,
                    atributo=campo,
                    valor=details.cleaned_data[campo],
                    usuario=usuario,
                )
                if alterado:
                    setattr(tipo, campo, details.cleaned_data[campo])
                alteracao |= alterado
            if alteracao:
                tipo.save()
            form = Tipo_equipamento.objects.all()
            return render(request, "listarTipo.html", {"form": form, "status": 1})
        else:
            # print('invalido')
            return render(request, "editarTipo.html", {"form": details})

@is_user
def listarTipo(request):
    status = request.GET.get("status")
    form = Tipo_equipamento.objects.all()
    return render(request, "listarTipo.html", {"form": form, "status": status})

@is_user
def baixarRelatorioEquipamentos(request):

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="relatorio.csv"'

    # Crie um objeto CSV Writer
    response.write("\ufeff".encode("utf8"))
    writer = csv.writer(response, delimiter=";")

    # Escreva o cabeçalho do arquivo CSV
    writer.writerow(
        [
            "Nome_equipamento",
            "modelo",
            "fabricante",
            "local",
            "tipo_equipamento",
            "data_compra",
            "data_ultima_calibracao",
            "usuario_cadastro",
            "data_cadastro",
            "patrimonio",
            "codigo",
            "custo_aquisição",
            "moeda",
            "projeto_compra",
            "responsavel",
            "potencia_eletrica",
            "tensao_eletrica",
            "nacionalidade",
            "data_ultima_atualizacao",
            "especificacao",
            "dados_adicionais",
            "ativo",
        ]
    )
    try:
        nome_equipamento = request.GET.get("filtro")
        q1 = Q(nome_equipamento__icontains=nome_equipamento)
        q2 = Q(codigo__icontains=nome_equipamento)
        q3 = Q(ativo=True)
        filtro = (q1 | q2) & q3
        equipamentos = Equipamento.objects.filter(filtro)
    except:
        equipamentos = Equipamento.objects.all()

    # Execute a consulta no banco de dados e adicione os resultados ao arquivo CSV
    for obj in equipamentos:
        writer.writerow(
            [
                obj.nome_equipamento,
                obj.modelo,
                obj.fabricante,
                obj.local,
                obj.tipo_equipamento,
                obj.data_compra,
                obj.data_ultima_calibracao,
                obj.usuario,
                obj.data_cadastro,
                obj.patrimonio,
                obj.codigo,
                obj.custo_aquisição,
                obj.custo_aquisição_currency,
                obj.projeto_compra,
                obj.responsavel,
                obj.potencia_eletrica,
                obj.tensao_eletrica,
                obj.nacionalidade,
                obj.data_ultima_atualizacao,
                obj.especificacao,
                obj.outros_dados,
                obj.ativo,
            ]
        )

    return response

@is_user
def cadastrarMaterial(request):
    usu = Usuario.objects.get(id=request.session.get("usuario"))
    # print(f"{usu.nome} acessou cadastro Cadastro Material")

    if request.method == "GET":
        form = materialCadastraForm
        return render(request, "cadastrarMaterial.html", {"form": form, "status": 0})
    else:
        details = materialCadastraForm(request.POST)
        if details.is_valid():
            details.save()
            material = Material_consumo.objects.get(
                nome_material=details.cleaned_data["nome_material"],
                fornecedor=details.cleaned_data["fornecedor"],
                especificacao_material=details.cleaned_data["especificacao_material"],
                unidade_material=details.cleaned_data["unidade_material"],
            )
            Log.cadastramento(usuario=usu, transacao="mc", objeto=material)

            form = materialCadastraForm

            return render(
                request, "cadastrarMaterial.html", {"form": form, "status": 1}
            )
        else:
            # print('invalido')
            return render(
                request, "cadastrarMaterial.html", {"form": details, "status": 2}
            )

@is_user
def editarMaterial(request):
    # print(f"{Usuario.objects.get(id=request.session.get('usuario')).nome} acessou Editar Material")
    if request.method == "GET":
        dados = Material_consumo.objects.get(id=request.GET.get("id")).dados_para_form()
        form = materialCadastraForm(initial=dados)
        return render(
            request,
            "editarMAterial.html",
            {"form": form, "id": request.GET.get("id"), "status": 0},
        )
    else:
        form = Material_consumo.objects.all()
        details = materialCadastraForm(request.POST)
        if details.is_valid():
            mat = Material_consumo.objects.get(id=details.cleaned_data["id"])
            usuario = Usuario.objects.get(id=request.session.get("usuario"))
            listaCampos = [
                "nome_material",
                "fornecedor",
                "especificacao_material",
                "unidade_material",
                "unidade_material",
                "simbolo_unidade_material",
            ]
            alteracao = False
            for campo in listaCampos:
                alterado = Log.foiAlterado(
                    transacao="mc",
                    objeto=mat,
                    atributo=campo,
                    valor=details.cleaned_data[campo],
                    usuario=usuario,
                )
                if alterado:
                    setattr(mat, campo, details.cleaned_data[campo])
                alteracao |= alterado
            if alteracao:
                mat.save()
            return render(request, "listarMateriais.html", {"form": form, "status": 1})
        else:
            return render(request, "listarMateriais.html", {"form": form, "status": 2})

@is_user
def listarMaterial(request):
    if request.method == "GET":
        form = Material_consumo.objects.all()
        return render(request, "listarMateriais.html", {"form": form, "status": 0})

@is_user
def cadastrarArquivo(request):

    if request.method == "POST":
        form = mediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = Media(
                nome=form.cleaned_data["nome"],
                documentos=form.cleaned_data["documentos"],
                equipamento=form.cleaned_data["equipamento"],
            )
            usuario = Usuario.objects.get(id=request.session.get("usuario"))
            media.save()
            equipamento= form.cleaned_data["equipamento"]
            utc=pytz.timezone(TIME_ZONE) # pytz.UTC
            equipamento.data_ultima_atualizaca=utc.localize( datetime.now())
            Log.cadastramento(
                objeto=media,
                usuario=usuario,
                transacao="me",
                equipamento=form.cleaned_data["equipamento"],
            )
            Log.foiAlterado(objeto=equipamento,
                            atributo="data_ultima_atualizacao",
                            valor=utc.localize( datetime.now()),
                            transacao="me",
                            usuario=usuario,
                            equipamento=equipamento,
                            nota_equipamento=None )
            equipamento.save()
            initial_data = {}
            initial_data['equipamento'] = equipamento.id
            form = mediaForm(initial=initial_data)
            render(request, "cadastrarArquivo.html", {"form": form})
        else:
            pass
            # print("Falhou")

    else:
        equipamento_id = request.GET.get('equipamento_id')
        if equipamento_id:
            initial_data = {}
            initial_data['equipamento'] = equipamento_id
            form = mediaForm(initial=initial_data)
        else :
            form = mediaForm()
    return render(request, "cadastrarArquivo.html", {"form": form})

@is_user
def excluiArquivo(request):

    if request.method == "GET":
        usuario = Usuario.objects.get(id=request.session.get("usuario"))
        media = Media.objects.get(id=request.GET.get("id"))
        id_equipamento = media.equipamento.id
        fullpath = os.path.normpath(os.path.join(MEDIA_ROOT, str(media.documentos)))
        caminho_backup = os.path.normpath(
            os.path.join(MEDIA_ROOT, "backup", os.path.basename(fullpath))
        )
        equipamento = Equipamento.objects.get(id=id_equipamento)
        try:
            os.replace(fullpath, caminho_backup)
            Log.exclusao(
                objeto=media, transacao="me", usuario=usuario, equipamento=equipamento
            )
            media.delete()
        except Exception as erro:
            return HttpResponse("<br><h2>Erro Ao excluir o arquivo</h2)<br>Favor entrar em contato com o Administrador do sistema")
        return redirect(f"/equipamentos/exibirDetalheEquipamento/?id={id_equipamento}")

    return HttpResponse("formulario de excluir arquivos")

@is_user
def download_arquivo(request):
    nome_arquivo = request.GET.get("filename") or request.POST.get("filename")
    fullpath = os.path.normpath(os.path.join(MEDIA_ROOT, nome_arquivo))
    if not fullpath.startswith(os.path.abspath(MEDIA_ROOT)):
        raise PermissionError("Acesso não permitido")

    with open(fullpath, "rb") as arquivo:
        figuras = ["jpg", "jpeg", "bmp", "gif", "svg", "png"]
        ext = nome_arquivo.split(".")[-1].lower()
        
        if ext in figuras:
            content_type = f'image/{ext if ext != "jpg" else "jpeg"}'  # Exceção para 'jpg' que deve ser 'jpeg'
            response = HttpResponse(arquivo.read(), content_type=content_type)
        else:
            response = HttpResponse(
                arquivo.read(), content_type="application/octet-stream"
            )
            filename = nome_arquivo.split("/")[-1]
            response["Content-Disposition"] = f'attachment; filename="{filename}"'

    return response

@is_admin
def excluirTipo(request):

    usuario = Usuario.objects.get(id=request.session.get("usuario"))
    if request.method == "GET":
        tipo_eq = request.GET.get("id")
        tipo_equipamento = Tipo_equipamento.objects.get(id=tipo_eq)
        equipamentos = Equipamento.objects.filter(tipo_equipamento=tipo_equipamento)
        return render(
            request,
            "excluirTipo.html",
            {
                "n": len(equipamentos),
                "equipamentos": equipamentos,
                "tipo": tipo_equipamento,
            },
        )
    elif request.method == "POST":
        tipo_eq = request.POST.get("id")
        tipo_equipamento = Tipo_equipamento.objects.get(id=tipo_eq)
        equipamentos = Equipamento.objects.filter(tipo_equipamento=tipo_equipamento)
        outros = Tipo_equipamento.objects.get(nome_tipo="Outros")
        if tipo_equipamento == outros:
            return redirect("/equipamentos/listarTipo/?status=50")

        for equipamento in equipamentos:
            # print(equipamento)
            Log.foiAlterado(
                transacao="eq",
                objeto=equipamento,
                atributo="tipo_equipamento",
                equipamento=equipamento,
                valor=outros,
                usuario=usuario,
            )
            equipamento.tipo_equipamento = outros
            equipamento.save()
        Log.exclusao(usuario=usuario, transacao="te", objeto=tipo_equipamento)
        tipo_equipamento.delete()

        return redirect("/equipamentos/listarTipo")
    return redirect(f"/equipamentos/?status=50")

@is_user
def excluirLocal(request):
    
    usuario = Usuario.objects.get(id=request.session.get("usuario"))
    tipo1 = Q(tipo="especialuser")
    tipo2 = Q(tipo="superuser")
    tipo3 = Q(tipo="admin")
    tipo = Tipo.objects.filter(tipo1 | tipo2 | tipo3)
    if usuario.tipo in tipo:
        if request.method == "GET":
            loc = request.GET.get("id")
            local = Local_instalacao.objects.get(id=loc)
            equipamentos = Equipamento.objects.filter(local=local)
            return render(
                request,
                "excluirLocal.html",
                {"n": len(equipamentos), "equipamentos": equipamentos, "local": local},
            )
        elif request.method == "POST":
            loc = request.POST.get("id")
            # print(loc)
            local = Local_instalacao.objects.get(id=loc)
            Log.exclusao(usuario=usuario, transacao="li", objeto=local)
            local.delete()
            return redirect("/equipamentos/listarLocais")
        return redirect(f"/equipamentos/?status=50")

@is_user
def consulta_dados_sistema(request):
    linhas, letras = acessaPastaRecursiva(BASE_DIR)
    agora = datetime.now()
    versao=dados_ambiente.versao
    data_consulta=f"{agora:%d/%m/%Y - %H:%M:%S}"
    contagem_tempo = (agora.year - 2023) * 12 + (agora.month - 6) + (agora.day) / 31
    if contagem_tempo <= 12:
        tempo = f"{converteBR(contagem_tempo,1)} meses"
    else:
        tempo = f"{converteBR(contagem_tempo/12,2)} anos"
    dic={'numero_caracteres': converteBR(letras),
         'numero_linhas': converteBR(linhas),
         'versao': versao,
         'data': data_consulta,
         'tempo': tempo,}
    return render(request,"exibirdadosSistema.html",dic)

@is_superuser
def listar_permissoes(request):
    equipamentos = Equipamento.objects.prefetch_related('autorizacao_equipamento_set__usuario').all()
    return render(request, 'listarPermissoes.html', {'equipamentos': equipamentos})

@is_superuser
def cadastrar_permissoes(request):
    usuario = Usuario.objects.get(id=request.session.get("usuario"))
    
    if request.method == "POST":
        details = cadastrarPermissaoForm(request.POST)

        if details.is_valid():
            usuario_cadastro = details.cleaned_data["usuario"]
            equipamento = details.cleaned_data["equipamento"]
            
            e = Autorizacao_equipamento(
                equipamento=equipamento,
                usuario=usuario_cadastro)
            e.save()

            Log.cadastramento(objeto=e, transacao="eq", usuario=usuario, equipamento=equipamento)

            form = cadastrarPermissaoForm() 
            return render(request, "cadastrarPermissao.html", {"form": form, "status": 1})
            
        
    form = cadastrarPermissaoForm()        
    return render(request, "cadastrarPermissao.html", {"form": form, "status": 0})
    

@is_superuser
def excluir_permissoes(request, id):
    permissao = get_object_or_404(Autorizacao_equipamento, id=id)
    usuario = Usuario.objects.get(id=request.session.get("usuario"))
    Log.exclusao(objeto=permissao, transacao="eq", usuario=usuario, equipamento=permissao.equipamento)
    permissao.delete()
    return redirect('listar_permissoes')  # Redireciona para a lista após exclusão
 