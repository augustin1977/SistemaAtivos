import os
from datetime import datetime, timedelta
import pandas as pd
import boxplot.boxplot2
from io import BytesIO
def converte_texto_numero(numero,tipo):
    digitos='0123456789'
    if (tipo==float):
        n=''
        ponto=0
        for digito in numero:
            # ~ print(digito,digito.isdigit(), digito in digitos)
            if (digito.isdigit()):
                n+=str(digito)
            elif ((digito=='.' or digito==",") and ponto==0):
                n+='.'
                ponto+=1
        if (n==''):
            return 0
        return float(n)
    if (tipo==int):
        n=''
        for i in numero:
            if i in digitos:
                n+=i
        return int(n)

def limpa_texto(texto):
	texto=texto.replace("\t"," ")
	texto=texto.replace(chr(8194)," ")
	anterior=" "
	texto_limpo=""
	for ch in texto:
		if not(ch==anterior and (ord(ch)<47 or ord(ch)>58)):
			texto_limpo+=ch
		anterior=ch
	return texto_limpo

def busca_separador(texto):
	texto_limpo=limpa_texto(texto)
	# ~ print(texto,texto_limpo)
	# ~ for i in texto_limpo:
		# ~ print(i, ord(i))
	for i in range(256):
		
		texto_alternativo=texto_limpo.split(chr(i))

		if len(texto_alternativo)==3:
			try:
				numero1=float(texto_alternativo[0])
				numero2=int(texto_alternativo[1])

				return chr(i)
			except:
				pass
	raise ValueError ("Separador não encontrado")
	return "\t"
class Dados:
    def __init__(self,valor_maximo,valor_minimo,gradiente_maximo,periodo_media,confianca_minima=90):
        self.dados=[]
        self.datas=[]
        self.confiancas=[]
        self.confianca_minima=confianca_minima=confianca_minima
        self.gradiente_maximo=gradiente_maximo
        self.periodo_media=periodo_media
        self.valor_maximo=valor_maximo
        self.valor_minimo=valor_minimo
    def carrega_dados(self,texto):
        dados_raw=texto.split("\n")
        separador=busca_separador(dados_raw[0])
        for linha in dados_raw:
            dados_compilados=limpa_texto(linha).split(separador)
            if len(dados_compilados)==3:
                valor=converte_texto_numero(dados_compilados[0],float)
                confianca=converte_texto_numero(dados_compilados[1],int)
                if ("\r" in dados_compilados[2]):
                    data=datetime.strptime(dados_compilados[2],"%Y-%m-%d %H:%M:%S\r")-timedelta(hours=2)
                else:
                    data=datetime.strptime(dados_compilados[2],"%Y-%m-%d %H:%M:%S")-timedelta(hours=2)
                self.dados.append(valor)
                self.datas.append(data)
                self.confiancas.append(confianca)

    def filtra_dados(self):
        n=0
        tamanho=len(self.dados)
        gradiente=0
        anterior=0
        while (n<tamanho):
            diff=self.datas[n]-self.datas[anterior]
            if diff.seconds>0:
                gradiente=abs((self.dados[n]-self.dados[anterior])/diff.seconds)
            else:
                gradiente=0
            # ~ print(n,anterior,self.dados[n], self.dados[anterior],gradiente,diff)
            if self.confiancas[n]<self.confianca_minima or self.dados[n]<self.valor_minimo or self.dados[n]>self.valor_maximo or gradiente>self.gradiente_maximo:
                self.confiancas.pop(n)
                self.dados.pop(n)
                self.datas.pop(n)
                tamanho-=1
            else:
                anterior=n
                n+=1
            
                
                
    def calcula_media_movel(self):
        dados=[]
        datas=[]
        for n,dado in enumerate(self.dados):
            dados.append(dado)
            datas.append(self.datas[n])
        self.dados=[]
        self.datas=[]
        self.confiancas=[]
        registro=0
        tempo_inicial=datas[0]
        n=0
        somavalores=0
        while(registro<len(dados)):
            diff=datas[registro]-tempo_inicial
            if (diff.seconds<self.periodo_media):
                somavalores+=dados[registro]
                n+=1
            elif n==0:
                self.dados.append(dados[registro])
                self.datas.append(tempo_inicial)
                self.confiancas.append(100)
                tempo_inicial=tempo_inicial+timedelta(seconds=self.periodo_media)
                n=0
                somavalores=0
                registro-=1
            else:
                self.datas.append(tempo_inicial)
                self.dados.append(somavalores/n)
                self.confiancas.append(100)
                tempo_inicial=tempo_inicial+timedelta(seconds=self.periodo_media)
                n=0
                somavalores=0
                
            registro+=1
    def retornaXLS(self,grandeza):
        dados={"datas":self.datas,grandeza:self.dados}
        df=pd.DataFrame(dados)
        buffer = BytesIO()
        file=df.to_excel(buffer,index=False)
        buffer.seek(0)
        return buffer
    def __str__(self):
        retorno=""
        for n,dado in enumerate(self.dados):
            retorno+=f"{n} - {dado} - {self.confiancas[n]} - {self.datas[n]}\n"
        return retorno

def geraXLS(file,opcoes):
   
    dados_raw=file.read()
    dados_raw=boxplot.boxplot2.try_decode(dados_raw)
    registro=Dados(valor_maximo=float(opcoes['valor_maximo']), 
                   valor_minimo=float(opcoes['valor_minimo']), 
                   gradiente_maximo=float(opcoes['gradiente_maximo']), 
                   periodo_media=float(opcoes['periodo_media']), 
                   confianca_minima=float(opcoes['confianca_minima']))
      
    registro.carrega_dados(dados_raw)
    registro.filtra_dados()
    registro.calcula_media_movel()
    return registro.retornaXLS(opcoes['grandeza'])


