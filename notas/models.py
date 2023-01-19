from django.db import models
from usuarios.models import *
from equipamentos.models import Equipamento,Material_consumo
"""Cadastro de disciplinas de manutenção ex(eletrica,mecaninca,eletronica,etc..."""
class Disciplina(models.Model):
    disciplina=models.CharField(max_length=50)
"""cadastra modos de falha para cada disciplina, ex(eletrica.motor_queimado, mecanica.quebra_mancal, etc).."""    
class Modo_Falha (models.Model):
    disciplina=models.ForeignKey(Disciplina, on_delete=models.DO_NOTHING)
    modo_falha=models.CharField(max_length=50)
"""Cadastra modos de falha possiveis de cada equipamento ex(eletrica.queima_resistencia.forno_eletrico)"""        
class Modo_falha_equipamento(models.Model):
    modo_falha=models.ForeignKey(Modo_Falha, on_delete=models.DO_NOTHING)
    equipamento=models.ForeignKey(Equipamento, on_delete=models.DO_NOTHING)

""" cadastra o material utilizado na nota_equipamento"""    
class Nota_material(models.Model):
    Material=models.ManyToManyField(Material_consumo)
    Quantidade=models.DecimalField(max_digits=12, decimal_places=2)
    
     
""" cadastra a nota do equipamento contendo a descrição do nota,equipamento, modo de falha,data do cadastro, se houve falha, calibração e lubrificação"""    
class Nota_equipamento(models.Model):
    descricao=models.TextField()
    equipamento=models.ForeignKey( Equipamento, on_delete=models.DO_NOTHING)
    modo_Falha_equipamento=models.ForeignKey(Modo_falha_equipamento, on_delete=models.DO_NOTHING)
    material=models.ManyToManyField(Nota_material)
    data_cadastro=models.DateTimeField(auto_now=True, auto_now_add=False)
    data_ocorrencia=models.DateField(auto_now=False, auto_now_add=False)
    falha=models.BooleanField()
    calibracao=models.BooleanField()
    lubrificao=models.BooleanField()
    usuario=models.ForeignKey( Usuario ,on_delete=models.DO_NOTHING)
