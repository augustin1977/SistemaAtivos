import pandas as pd
import boxplot.boxplot2
from io import BytesIO
from datetime import datetime

def converte_data(dado):
   return datetime.strptime(dado,"%m/%d/%Y %H:%M:%S")

class Dados:
    def __init__(self):
        self._record=[]
        self._dataHora=[]
        self._temperatura=[]
        self._forca=[]
        self._troca_agua=[]
        
        
    def carrega_dados(self,dados):
        dados=dados.split("\n")
        for i,dado in enumerate(dados):
            dado_aux=dado.split(",")
            if i>0:
                if dado:
                    self._record.append(int(dado_aux[0]))
                    self._dataHora.append(converte_data(dado_aux[1]+" "+dado_aux[2]))
                    self._temperatura.append(float(dado_aux[3]))
                    self._forca.append(float(dado_aux[4]))
                    self._troca_agua.append(int(dado_aux[5]))
                
    def retorna_dados(self):
        dados={"record":self._record,
            "Data_Hora": self._dataHora,
            "temperatura":self._temperatura,
            "forca":self._forca,
            "troca_agua":self._troca_agua
            }
        
        return dados

    def retornaXLS(self):
        df=pd.DataFrame(self.retorna_dados())
        buffer = BytesIO()
        file=df.to_excel(buffer,index=False)
        buffer.seek(0)

        return buffer
        

def geraXLS(file):
    dados_raw=file.read()
    dados_raw=boxplot.boxplot2.try_decode(dados_raw)
    dados=Dados()
    print(dados.retorna_dados())
    dados.carrega_dados(dados_raw)
    return dados.retornaXLS()
