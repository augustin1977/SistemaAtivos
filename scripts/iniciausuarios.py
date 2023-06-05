import os
import re
from usuarios.views import *
from usuarios.models import *

def run():
	print("importando dados do excel!")
	caminho=os.getcwd()
	#print(caminho)
	try:
		
		nome_arquivo=os.path.join(caminho,"Lista_LPM.txt")
		arquivo=open(nome_arquivo,"r")
		linha=arquivo.readline()
		linha=arquivo.readline()
		linha=arquivo.readline()
		linha=arquivo.readline()
		i=0
		remetentes={}
		while(linha):
			linha=arquivo.readline().strip()
			vetor=linha.split('\t')
			if vetor[0]:
				remetentes[vetor[0]]=vetor[1]
			i+=1
		arquivo.close()
	except Exception as erro:
		print(erro)
	pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
	tipo=Tipo.objects.filter(tipo="user")
	print(user)
	
	for nome in remetentes:
		if nome and remetentes[nome]:
			if re.search(pattern, remetentes[nome]):
				print(nome,remetentes[nome])
				senha=gerasenha(12)
				usuario=Usuario(nome=nome,chapa=0,email=remetentes[nome],senha=senha,tipo=tipo[0],primeiro_acesso=True,ativo=True)
				usuario.save()
			else:
				print("##################Email incorreto##################")

		else:
			print("##################Errro##################")


