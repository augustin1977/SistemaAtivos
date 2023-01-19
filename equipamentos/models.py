from django.db import models
from usuarios.models import *
from equipamentos.models import *

class Fabricante(models.Model):
    nome_fabricante=models.CharField(max_length=80)
    endereco_fabricante=models.CharField(max_length=180,null=True, blank=True)
    nome_contato_fabricante=models.CharField(max_length=80,null=True, blank=True)
    telefone_contato=models.CharField(max_length=80,null=True, blank=True)
    email_contato_fabricante=models.EmailField(max_length=254,null=True, blank=True)
    site_Fabricante=models.CharField(max_length=254,null=True, blank=True)
    dados_adicionais=models.TextField(null=True, blank=True)

class Local_instalacao(models.Model):
    predio=models.CharField(max_length=10)
    piso=models.CharField(max_length=10)
    sala=models.CharField(max_length=10)
    armario=models.CharField(max_length=10)
    prateleira=models.CharField(max_length=10)
    apelido_local=models.CharField(max_length=50)
    
class Tipo_equipamento(models.Model):
    nome_tipo=models.CharField(max_length=50)
    descricao_tipo=models.TextField(null=True, blank=True)    


class Equipamento(models.Model):
    nome_equipamento=models.CharField(max_length=80)
    modelo=models.CharField(max_length=80)
    fabricante=models.ForeignKey(Fabricante, on_delete=models.DO_NOTHING)
    local=models.ForeignKey(Local_instalacao, on_delete=models.DO_NOTHING)
    tipo_equipamento=models.ForeignKey(Tipo_equipamento, on_delete=models.DO_NOTHING)
    data_compra=models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)
    data_ultima_calibracao=models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)
    usuario=models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    data_cadastro=models.DateTimeField(auto_now=True, auto_now_add=False)
    patrimonio=models.CharField(max_length=30)
    
class Material_consumo(models.Model):
    nome_material=models.CharField(max_length=50)
    fornecedor=models.ForeignKey(Fabricante,on_delete=models.DO_NOTHING, null=True, blank=True)
    especificacao_material=models.TextField(null=True, blank=True)
    unidade_material=models.CharField(max_length=10)
    simbolo_unidade_material=models.CharField(max_length=5)


class media(models.Model):
    media=models.ImageField(upload_to ='images/')
    equipamento=models.ForeignKey(Equipamento,on_delete=models.DO_NOTHING, null=False, blank=False)
