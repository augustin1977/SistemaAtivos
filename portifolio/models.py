from django.db import models
from usuarios.models import *
from equipamentos.models import Local_instalacao


class Cor(models.Model):
    nome=models.CharField(max_length=255, unique=True)
    tonalidade=models.CharField(max_length=9,unique=True) # Exemplo: #RRGGBBOO (Red, Green, Blue, Opacity)
    ativa=models.BooleanField(default=True)
    def __str__(self):
        return f"{self.nome} - {'Ativa' if self.ativa else 'Inativa'}" 
    
class Projeto(models.Model):
    nome=models.CharField(max_length=255,unique=True)
    cliente=models.CharField(max_length=255)
    data_criacao=models.DateTimeField(auto_now_add=True)
    ativo=models.BooleanField(default=True)
    cor=models.ForeignKey(Cor, on_delete=models.PROTECT, null=False, blank=False)
    responsavel=models.ForeignKey(Usuario, on_delete=models.PROTECT, null=False, blank=False)
    def __str__(self):
        return f"{self.nome} - {self.cliente} - {self.cor.nome} - {self.Responsavel.nome}"
class Amostra(models.Model):
    nome=models.CharField(max_length=255)
    projeto=models.ForeignKey(Projeto, on_delete=models.CASCADE, null=False, blank=False)
    data_cadastro=models.DateTimeField(auto_now_add=True)
    data_alteracao=models.DateTimeField(auto_now=True)
    data_recebimento=models.DateField(null=False, blank=False)
    data_fim=models.DateField(null=True, blank=True)
    prazo_dias=models.IntegerField()
    def __str__(self):
        return f"{self.nome} - {self.projeto.nome}"
class Etiqueta(models.Model):
    amostra=models.ForeignKey(Amostra, on_delete=models.CASCADE, null=False, blank=False)
    data_criacao=models.DateTimeField(auto_now_add=True)
    data_alteracao=models.DateTimeField(auto_now=True)
    local_instalacao=models.ForeignKey(Local_instalacao, on_delete=models.PROTECT, null=False, blank=False)
    massa=models.DecimalField(max_digits=10, decimal_places=3)
    codigo_humano=models.CharField(max_length=255,unique=True)
    codigo_numerico=models.CharField(max_length=255, unique=True)
    observacao=models.TextField(blank=True)
    def __str__(self):
        cor_nome = self.amostra.projeto.cor.nome
        return f"{self.codigo_humano} - {self.amostra.nome} - {self.codigo_numerico} - {cor_nome}"
