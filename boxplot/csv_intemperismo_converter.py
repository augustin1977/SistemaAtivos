import pandas as pd
import boxplot.boxplot2
from io import BytesIO

def converte_data(dado):
    data=dado.split("/")
    return f"{data[1]}/{data[0]}/{data[2]}"

class Dados:
    def __init__(self):
        self._record=[]
        self._data=[]
        self._hora=[]
        self._temperatura=[]
        self._forca=[]
        self._troca_agua=[]
        #self._dataHora=[]
        
    def carrega_dados(self,dados):
        dados=dados.split("\n")
        for i,dado in enumerate(dados):
            dado_aux=dado.split(",")
            if i>0:
                if dado:
                    self._record.append(int(dado_aux[0]))
                    data=converte_data(dado_aux[1])
                    hora=dado_aux[2]
                    self._data.append(data)
                    self._hora.append(hora)
                    #self._dataHora.append(data+" "+hora)
                    self._temperatura.append(float(dado_aux[3]))
                    self._forca.append(float(dado_aux[4]))
                    self._troca_agua.append(int(dado_aux[5]))
                
    def retorna_dados(self):
        return {"record":self._record,
            "Data": self._data,
            "hora":self._hora,
            "temperatura":self._temperatura,
            "forca":self._forca,
            "troca_agua":self._troca_agua
            }

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
    dados.carrega_dados(dados_raw)
    return dados.retornaXLS()
