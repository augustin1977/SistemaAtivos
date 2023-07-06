import os
class Pasta:
	"""Cria estrutura de dados para funcionamento das funções de calculo do nuero de linhas e caracteres"""
	def __init__(self,caminho):
		self.caminho=os.path.join(caminho)
		self.arquivos=[]
		self.subpastas=[]
		self.atualiza_caminho()
	def atualiza_caminho(self):
		lista = os.listdir(self.caminho)
		for arquivo in lista:

			if os.path.isfile(os.path.join(self.caminho,arquivo)):
				self.arquivos.append(arquivo)
			if os.path.isdir(os.path.join(self.caminho,arquivo)):
				self.subpastas.append(Pasta(os.path.join(self.caminho,arquivo)))
	def __str__(self):
		return str(self.arquivos)
def converteBR(numero):
	"""Converte numero padão americano em numero padrão BR"""
	tipo=type(numero)
	if not(tipo==int or tipo==float):
		return "erro - Valor não numerico -> "+str(numero)
	else :
		string=f"{numero:_}"
		string=string.replace(".",",")
		string= string.replace('_','.')
	return string
	
	
def acessaPastaRecursiva(pasta):
	"""Faz o acesso a todas as subpastas de forma recursiva e retorna os valores das linhas e caracteres"""
	cLinha=0
	cletras=0
	contadorLinha = 0
	contadorletras = 0
	pasta=Pasta(pasta)

	cLinha,cletras=acessarPastaecontar(pasta.caminho)
	contadorLinha+=cLinha
	contadorletras+=cletras
	if pasta.subpastas:
		for p in pasta.subpastas:
			cLinha,cletras=acessaPastaRecursiva(p.caminho)
			contadorLinha+=cLinha
			contadorletras+=cletras
			
	return contadorLinha,contadorletras

def acessarPastaecontar(pasta):
	contadorLinha = 0
	contadorletras = 0
	pasta=Pasta(pasta)
	for p in pasta.arquivos:
		cLinha=0
		cletras=0
		if p[-2:]=='py' or p[-3:]=='txt' or p[-4:]=='html' or p[-3:]=='htm' or p[-2:]=='md':
			cLinha,cletras=contar_linhas_com_conteudo(os.path.join(pasta.caminho,p))
			contadorLinha+=cLinha
			contadorletras+=cletras
		#print(p,c)
	return contadorLinha,contadorletras

def contar_linhas_com_conteudo(caminho_arquivo):
    contadorLinha = 0
    contadorletras=0
    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            linha = linha.strip()  
            if linha and not linha.isspace():
                contadorLinha += 1
                contadorletras+=len(linha)
                #print(linha)
    return contadorLinha,contadorletras




