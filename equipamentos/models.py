# -*- coding: utf-8 -*-

from django.db import models
from usuarios.models import *
from equipamentos.models import *
import datetime
from django.forms import ValidationError 
from djmoney.models.fields import MoneyField



class Fabricante(models.Model):
    nome_fabricante=models.CharField(max_length=80)
    endereco_fabricante=models.CharField(max_length=180,null=True, blank=True)
    nome_contato_fabricante=models.CharField(max_length=80,null=True, blank=True)
    telefone_contato=models.CharField(max_length=80,null=True, blank=True)
    email_contato_fabricante=models.EmailField(max_length=254,null=True, blank=True)
    site_Fabricante=models.CharField(max_length=254,null=True, blank=True)
    dados_adicionais=models.TextField(null=True, blank=True)
    def __str__(self):
        return str(self.nome_fabricante)
    class Meta:
        ordering = ['nome_fabricante']

class Local_instalacao(models.Model):
    laboratorio=models.CharField(max_length=30)
    predio=models.CharField(max_length=50)
    piso=models.CharField(max_length=80)
    sala=models.CharField(max_length=80,null=True, blank=True)
    armario=models.CharField(max_length=80,null=True, blank=True)
    prateleira=models.CharField(max_length=50,null=True, blank=True)
    apelido_local=models.CharField(max_length=50,null=True, blank=True)
    class Meta:
        ordering = ['predio','piso','-sala','-armario','prateleira']
    def __str__(self):
        retorno= self.laboratorio+"."+self.predio
        if self.piso:
            retorno+="."+self.piso
        if self.sala:
            retorno+="."+self.sala
        if self.armario:
            retorno+="."+self.armario
        if self.prateleira:
            retorno+="."+self.prateleira
        return  retorno
    def dados_para_form(self):
        return {'id':self.id, 'laboratorio':self.laboratorio,'predio':self.predio,"piso":self.piso,"sala":self.sala,
        "armario":self.armario,'prateleira':self.prateleira}

    
    
class Tipo_equipamento(models.Model):
    nome_tipo=models.CharField(max_length=50)
    sigla=models.CharField(max_length=3,unique=True)
    descricao_tipo=models.TextField(null=True, blank=True)    
    def __str__(self):
        return str(self.nome_tipo)
    class Meta:
        ordering = ['nome_tipo']
    def dados_para_form(self):
        return {'id':self.id, 'nome_tipo':self.nome_tipo,"descricao_tipo":self.descricao_tipo}

class Material_consumo(models.Model):
    nome_material=models.CharField(max_length=70)
    fornecedor=models.ForeignKey(Fabricante,on_delete=models.SET_NULL, null=True, blank=True)
    especificacao_material=models.TextField(null=True, blank=True)
    unidade_material=models.CharField(max_length=10)
    simbolo_unidade_material=models.CharField(max_length=5)
    def dados_para_form(self):
        return {"id":self.id,"nome_material":self.nome_material,"fornecedor":self.fornecedor,
        "especificacao_material":self.especificacao_material,"unidade_material":self.unidade_material,
        "simbolo_unidade_material":self.simbolo_unidade_material}
    def __str__(self):
        return self.nome_material + "-"+ self.especificacao_material
    class Meta:
        ordering = ['nome_material']


class Equipamento(models.Model):
    nome_equipamento=models.CharField(max_length=80)
    modelo=models.CharField(max_length=80,null=True, blank=True)
    fabricante=models.ForeignKey(Fabricante, on_delete=models.DO_NOTHING,null=True, blank=True)
    local=models.ForeignKey(Local_instalacao, on_delete=models.DO_NOTHING,null=True, blank=True)
    tipo_equipamento=models.ForeignKey(Tipo_equipamento, on_delete=models.DO_NOTHING)
    data_compra=models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    data_ultima_calibracao=models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    usuario=models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    data_cadastro=models.DateTimeField(auto_now=True, auto_now_add=False)
    patrimonio=models.CharField(max_length=30,null=True, blank=True)
    material_consumo=models.ManyToManyField(Material_consumo,  blank=True)
    codigo=models.CharField(max_length=9,null=True, blank=True,unique=True)
    custo_aquisição=MoneyField(max_digits=25, decimal_places=2, default_currency='BRL')
    responsavel=models.CharField(max_length=50,null=True, blank=True)
    potencia_eletrica=models.CharField(max_length=30,null=True, blank=True)
    nacionalidade=models.CharField(max_length=50,null=True, blank=True)
    data_ultima_atualizacao=models.DateTimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
    tensao_eletrica=models.CharField(max_length=30,null=True, blank=True)
    projeto_compra=models.CharField(max_length=50,null=True, blank=True)
    especificacao=models.TextField(null=True, blank=True)
    outros_dados=models.TextField(null=True, blank=True)

    def dados_para_form(self):
        return {"id":self.id,"nome_equipamento":self.nome_equipamento,"modelo":self.modelo,"fabricante":self.fabricante,
        "local":self.local,"tipo_equipamento":self.tipo_equipamento,"data_compra":self.data_compra,
        "data_ultima_calibracao":self.data_ultima_calibracao,"usuario":self.usuario,"patrimonio":self.patrimonio,"codigo":self.codigo,
        "material_consumo":Material_consumo.objects.filter(equipamento__id=self.id),'custo_aquisição':self.custo_aquisição,
         'responsavel':self.responsavel,'potencia_eletrica':self.potencia_eletrica,'nacionalidade':self.nacionalidade,'tensao_eletrica':self.tensao_eletrica,
         'data_ultima_atualizacao':self.data_ultima_atualizacao,'projeto_compra':self.projeto_compra,'especificacao':self.especificacao,
         'outros_dados':self.outros_dados}

    class Meta:
        ordering = ['nome_equipamento']
    def __str__(self):
        return str(self.nome_equipamento)+"-"+str(self.codigo)
    


class Media(models.Model):

    nome=models.CharField(max_length=50)
    media=models.ImageField(upload_to ='',null=True, blank=True)
    documentos= models.FileField(upload_to ='',null=True, blank=True)
    equipamento=models.ForeignKey(Equipamento,on_delete=models.DO_NOTHING, null=False, blank=False)

    def __str__(self):
        return self.nome