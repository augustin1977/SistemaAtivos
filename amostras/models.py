from django.db import models
from usuarios.models import *
from equipamentos.models import *


class Fator(models.Model):
    """Criação do banco de dade de fator de conversão"""
    simbolo=models.CharField(max_length=5,unique=True)
    fator=models.FloatField(default=1.0,verbose_name="Fator de conversão")
    def __str__(self):
        return str(self.simbolo)


class Unidade(models.Model):
    unidade=models.CharField(max_length=20,unique=True)
    simbolo=models.CharField(max_length=5,unique=True)
    # fator_multiplicador=models.ForeignKey(Fator, on_delete=models.DO_NOTHING, null=False, blank=False, verbose_name="Multiplicador")
    
    def __str__(self):
        return str(self.simbolo)

class Amostra(models.Model):
    """Criação do banco de dados de amostrtas"""
    nome=models.CharField(max_length=70,null=False, blank=False, verbose_name="Nome da amostra")
    descricao=models.TextField(null=False, blank=False,verbose_name="Descrição")
    data=models.DateTimeField(auto_now=False, auto_now_add=False, null=False, blank=False, verbose_name="Data de Recebimento")
    especificacao_material=models.TextField(null=False, blank=False, verbose_name="Especificação")
    quantidade=models.DecimalField(max_digits=20, decimal_places=6, null=False, blank=False, verbose_name="Quantidade")
    fator_multiplicador=models.ForeignKey(Fator, on_delete=models.DO_NOTHING, null=False, blank=False, verbose_name="Multiplicador")
    unidade=models.ForeignKey(Unidade, on_delete=models.DO_NOTHING, null=False, blank=False, verbose_name="Unidade de medida")
    data_cadastro=models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name="Data de cadastro")
    data_atualizacao=models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True, verbose_name="Data de atualização")
    localizacao=models.ForeignKey(Local_instalacao, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="Localização")
    def __str__(self):
            return f"{self.nome} - {self.quantidade} {self.fator_multiplicador.simbolo}{self.unidade.simbolo}"