from django.db import models
from usuarios.models import *
from equipamentos.models import Equipamento
from notas.models import Nota_equipamento

class Log(models.Model):
    lista_transacoes=[('eq','Equipamento'),('te','Tipo Equipamento'),('fn','Fornecedor'),('li','Local Instalação'),('mc','Material Consumo'),
                        ('me','media'),('dc','Disciplina de Manutenção'),('mf','Modo de Falha'),('me','Modo de falha Equipamento'),
                        ('nm','Nota Material'),('ne','Nota Equipamento'),('us','usuario'),('tu','Tipo de Usuario')]
    lista_movimentos=[('cd','Cadastro'),('lt','Listagem'),('ed','Edição'),('dl','Delete')]
    transacao=models.CharField(choices=lista_transacoes,max_length=10)
    movimento=models.CharField(choices=lista_movimentos,max_length=10)
    data_cadastro=models.DateTimeField(auto_now=True, auto_now_add=False)
    usuario=models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    equipamento=models.ForeignKey(Equipamento,on_delete=models.DO_NOTHING, null=True)
    Nota_equipamento=models.ForeignKey(Nota_equipamento,on_delete=models.DO_NOTHING,null=True)
    alteracao=models.CharField(max_length=30)
    
    def __str__(self):
        retorno= self.transacao
        if self.usuario:
            retorno+="."+self.usuario
        if self.equipamento:
            retorno+="."+self.equipamento
        if self.Nota_equipamento:
            retorno+="."+self.Nota_equipamento
        if self.alteracao:
            retorno+="."+self.alteracao
        return  retorno
