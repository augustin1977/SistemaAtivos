from notas.models import *
from equipamentos.models import *
from django.db.models import Q
def carrega_novos_modos_falha(novadisciplina):
    disciplina=Disciplina.objects.filter(disciplina=novadisciplina)
    modos_falha=Modo_Falha.objects.filter(disciplina=disciplina[0])
    equipamentos=Equipamento.objects.all()
    for equipamento in equipamentos:
        filtro1 = Q(equipamento=equipamento)
        for modo_falha in modos_falha:
            filtro2= Q(modo_falha=modo_falha)
            if not Modo_falha_equipamento.objects.filter(filtro1 & filtro2):
                modo_falha_equipamento=Modo_falha_equipamento(equipamento=equipamento,modo_falha=modo_falha)
                modo_falha_equipamento.save()
                print(f"Cadastrado {modo_falha} no {equipamento}")
            
print("carregando novos modos de falha")
print("Melhoria....")
carrega_novos_modos_falha("Melhoria")  
print("Movimentação....")      
carrega_novos_modos_falha("Movimentação")
