from django.db import models
from usuarios.models import *
from equipamentos.models import Equipamento
from notas.models import Nota_equipamento

class Log(models.Model):
    lista_transacoes=[('eq','Equipamento'),('te','Tipo Equipamento'),('fn','Fornecedor'),('li','Local Instalação'),('mc','Material Consumo'),
                        ('me','media'),('dc','Disciplina de Manutenção'),('mf','Modo de Falha'),('me','Modo de falha Equipamento'),
                        ('nm','Nota Material'),('ne','Nota Equipamento'),('us','usuario'),('tu','Tipo de Usuario'),("rt","Relatório")]
    lista_movimentos=[('cd','Cadastro'),('lt','Listagem'),('ed','Edição'),('dl','Delete'),('lo','logOn'),('lf','logOff')]
    transacao=models.CharField(choices=lista_transacoes,max_length=10)
    movimento=models.CharField(choices=lista_movimentos,max_length=10)
    data_cadastro=models.DateTimeField(auto_now=True, auto_now_add=False)
    usuario=models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    equipamento=models.ForeignKey(Equipamento,on_delete=models.DO_NOTHING, null=True,blank=True)
    nota_equipamento=models.ForeignKey(Nota_equipamento,on_delete=models.DO_NOTHING,null=True,blank=True)
    alteracao=models.TextField()
    class Meta:
        ordering = ['-data_cadastro','usuario','nota_equipamento','transacao','movimento']
    def __str__(self):
        retorno= str(self.data_cadastro)+"."+self.transacao+ "."+self.movimento
        if self.usuario:
            retorno+="."+str(self.usuario)
        if self.equipamento:
            retorno+="."+str(self.equipamento)
        if self.nota_equipamento:
            retorno+="."+str(self.nota_equipamento)
        if self.alteracao:
            retorno+="."+self.alteracao
        return  retorno
    
