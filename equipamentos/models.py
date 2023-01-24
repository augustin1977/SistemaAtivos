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
    def __str__(self):
        return str(self.nome_fabricante)
    class Meta:
        ordering = ['nome_fabricante']

class Local_instalacao(models.Model):
    predio=models.CharField(max_length=30)
    piso=models.CharField(max_length=15)
    sala=models.CharField(max_length=15,null=True, blank=True)
    armario=models.CharField(max_length=15,null=True, blank=True)
    prateleira=models.CharField(max_length=15,null=True, blank=True)
    apelido_local=models.CharField(max_length=50,null=True, blank=True)
    def __str__(self):
        retorno= self.predio
        if self.piso:
            retorno+="."+self.piso
        if self.sala:
            retorno+="."+self.sala
        if self.armario:
            retorno+="."+self.armario
        if self.prateleira:
            retorno+="."+self.prateleira
        return  retorno
    class Meta:
        ordering = ['-predio','piso','-sala','-armario','prateleira']
    
class Tipo_equipamento(models.Model):
    nome_tipo=models.CharField(max_length=50)
    descricao_tipo=models.TextField(null=True, blank=True)    
    def __str__(self):
        return str(self.nome_tipo)
    class Meta:
        ordering = ['nome_tipo']

class Material_consumo(models.Model):
    nome_material=models.CharField(max_length=70)
    fornecedor=models.ForeignKey(Fabricante,on_delete=models.SET_NULL, null=True, blank=True)
    especificacao_material=models.TextField(null=True, blank=True)
    unidade_material=models.CharField(max_length=10)
    simbolo_unidade_material=models.CharField(max_length=5)
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
    patrimonio=models.CharField(max_length=30)
    material_consumo=models.ManyToManyField(Material_consumo,  blank=True)
    codigo=models.CharField(max_length=40)
    class Meta:
        ordering = ['nome_equipamento']
    def __str__(self):
        return str(self.nome_equipamento)
    


class Media(models.Model):

    nome=models.CharField(max_length=50)
    media=models.ImageField(upload_to ='',null=True, blank=True)
    documentos= models.FileField(upload_to ='',null=True, blank=True)
    equipamento=models.ForeignKey(Equipamento,on_delete=models.DO_NOTHING, null=False, blank=False)

    def __str__(self):
        return self.nome