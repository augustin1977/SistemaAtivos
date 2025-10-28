from usuarios.models import *
from equipamentos.models import *
from usuarios.views import *
from portifolio.models import *
from notas.models import *
from django.conf import settings
from django.db.models import Q
from django.core.files import File
import pytz
import datetime
import pandas as pd
import os
import shutil


# ======================
# Funções Modulares
# ======================

def criar_tipos_usuarios():
    print("Criando tipos de usuários...")
    tipos = ["admin", "user", "superuser", "especialuser"]
    for tipo in tipos:
        obj, created = Tipo.objects.get_or_create(tipo=tipo)
        if created:
            print(f"→ Tipo criado: {tipo}")
        else:
            print(f"→ Tipo '{tipo}' já existe.")
    print("Tipos de usuários OK!\n")


def criar_usuario_sistema():
    print("Verificando usuário do sistema...")
    if not Usuario.objects.filter(nome="System").exists():
        print("→ Criando usuário do sistema.")
        senha = gera_senha(12)
        usuario = Usuario.objects.create(
            nome="System",
            email="system@ipt.br",
            tipo=Tipo.objects.get(tipo="admin"),
            primeiro_acesso=True,
            senha=senha,
            ativo=True,
        )
        print(f"→ Usuário 'System' criado: {usuario.email}")
    else:
        print("→ Usuário 'System' já existe.\n")


def criar_disciplinas():
    print("Criando disciplinas e modos de falha...")
    disciplinas = {
        "Elétrica": [
            "Defeito Painel", "Problema no cabo Alimentação", "Sem energia",
            "Fusivel Queimado", "Falha Motor", "Preventiva",
            "Falha na botoeira", "Falha no inversor", "Falha Disjuntor",
            "Resistencia Queimada", "outros"
        ],
        "Mecânica": [
            "Quebra de componente", "Falha estrutural", "Travamento",
            "Entupimento", "Lubrificação", "vazamento", "calibração",
            "Preventiva", "Ajustes", "outros"
        ],
        "Hidraulica": [
            "Mangueira vazando/rompida", "vazamento", "falta de oleo",
            "baixa pressão de óleo", "Manômetro", "Entupimento",
            "preventiva", "Calibração", "Sensor vazão", "outros"
        ],
        "Civil": ["Problema Base fixação", "Chumbamento", "Pintura", "outros"],
        "Eletrônica": [
            "Placa queimada/defeito", "botão com defeito",
            "Falha sensor", "PLC travado/queimado", "Preventiva",
            "Calibração", "outros"
        ],
        "Informática": [
            "Erro sistema Operacional", "computador não liga/inicia", "Tela Azul",
            "Sistema travado", "Erro comunicação", "calibração", "outros"
        ],
        "Geral": ["Calibração", "Falha geral", "problema não identificado", "outros"],
        "Outros": ["Outros", "Falta energia", "Equipamento sem componentes"],
    }

    for nome, modos in disciplinas.items():
        d, created = Disciplina.objects.get_or_create(disciplina=nome)
        if created:
            print(f"→ Disciplina criada: {nome}")
        else:
            print(f"→ Disciplina '{nome}' já existe.")
        for modo in modos:
            m, created = Modo_Falha.objects.get_or_create(
                disciplina=d,
                modo_falha=modo.capitalize()
            )
            if created:
                print(f"  ↳ Modo criado: {modo}")
    print("Disciplinas e modos de falha OK!\n")


def criar_locais_basicos():
    print("Verificando local 'Descarte'...")
    Local_instalacao.objects.get_or_create(
        laboratorio="LPM",
        defaults=dict(
            predio="Descarte",
            piso="Descarte",
            sala="Descarte",
            armario="Descarte",
            prateleira="Descarte",
            apelido_local="Descarte"
        )
    )
    print("Local 'Descarte' OK!\n")


def criar_tipos_equipamento_basicos():
    print("Verificando tipo 'Outros'...")
    Tipo_equipamento.objects.get_or_create(
        nome_tipo="Outros",
        defaults=dict(sigla="OUT", descricao_tipo="Outros equipamentos")
    )
    print("Tipo de equipamento básico OK!\n")


def criar_cores_basicas():
    print("Criando cores básicas...")
    cores = {
    "Azul": "#0000FF",
    "Azul claro": "#5ADAFF",
    "Azul escuro": "#101079",
    "Cinza": "#708091",
    "Cinza claro": "#B7B7BC",
    "Cinza escuro": "#35353D",
    "Laranja": "#FF8C00",
    "Laranja claro": "#FFDBBB",
    "Marrom": "#8B4513",
    "Marrom claro": "#CAAA81",
    "Preto": "#000000",
    "Roxo": "#7B057B",
    "Verde": "#00FF00",
    "Verde claro": "#BAFFBA",
    "Verde escuro": "#128912",
    "Vermelho": "#FF0000",
    "Amarelo":"#FFFF00",
    "Ciano":"#00FFFF",
    "Magenta":"#FF00FF",
    "Oliva":"#808000",
    "Ouro":"#FFD700",
    "Amarelo Claro":"#FFFF8E",
}
    for nome, tonalidade in cores.items():
        cor, created = Cor.objects.get_or_create(
            nome=nome, defaults={"tonalidade": tonalidade, "ativa": True}
        )
        if created:
            print(f"→ Cor criada: {nome}")
        else:
            print(f"→ Cor '{nome}' já existe.")
    print("Cores OK!\n")


def criar_projetos_iniciais():
    print("Criando projetos iniciais...")
    system_user = Usuario.objects.get(nome="System")
    cor_padrao = Cor.objects.first()
    projetos = [
        {"nome": "Projeto Alfa", "cliente": "Cliente X"},
        {"nome": "Projeto Beta", "cliente": "Cliente Y"},
    ]
    for p in projetos:
        obj, created = Projeto.objects.get_or_create(
            nome=p["nome"],
            defaults={"cliente": p["cliente"], "cor": cor_padrao, "responsavel": system_user}
        )
        if created:
            print(f"→ Projeto criado: {p['nome']}")
        else:
            print(f"→ Projeto '{p['nome']}' já existe.")
    print("Projetos OK!\n")


def criar_sequencia_etiqueta():
    print("Verificando sequência de etiquetas...")
    SequenciaEtiqueta.objects.get_or_create(id=1, defaults={"proximo_numero": 1})
    print("Sequência de etiquetas OK!\n")


# ======================
# Função Principal
# ======================

def run():
    print("\n=== Iniciando configuração inicial do sistema ===\n")
    criar_tipos_usuarios()
    criar_usuario_sistema()
    #criar_disciplinas()
    #criar_locais_basicos()
    #criar_tipos_equipamento_basicos()
    criar_cores_basicas()
    # criar_projetos_iniciais()
    # criar_sequencia_etiqueta()
    print("\n=== Configuração concluída com sucesso! ===\n")
