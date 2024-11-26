import pandas as pd
import boxplot.boxplot2
from io import BytesIO
from datetime import datetime

def converte_data(dado):
   return datetime.strptime(dado,"%m/%d/%Y %H:%M:%S")

class Dados:
    def __init__(self,opcao):
        self._record=[]
        self._dataHora=[]
        self._temperatura=[]
        self._forca=[]
        self._troca_agua=[]
        self._posicao=[]
        self._ph=[]
        self._agua_ligada=[]
        self._agua_desligada=[]
        self._nobreak=[]
        self._peso=[]
        self._opcao=opcao
        
        
    def carrega_dados(self,dados):
        dados=dados.split("\n")
        for i,dado in enumerate(dados):
            dado_aux=dado.split(",")
            # print(dado,self._opcao)
            if i>0:
                if self._opcao=="Intemperismo":
                    
                    if dado:
                        self._record.append(int(dado_aux[0]))
                        self._dataHora.append(converte_data(dado_aux[1]+" "+dado_aux[2]))
                        self._temperatura.append(float(dado_aux[3]))
                        self._forca.append(float(dado_aux[4]))
                        self._posicao.append(float(dado_aux[5]))
                        self._ph.append(float(dado_aux[6]))
                        if int(dado_aux[8])==1:
                            self._troca_agua.append("Sim")
                        else:
                            self._troca_agua.append("Não")
                        if int(dado_aux[9])==1:
                            self._nobreak.append("Energia")
                        else:
                            self._nobreak.append("No_Break")
                        
                        agua=dado_aux[7].replace('"',"").split("#")
                        self._agua_ligada=int(agua[1])
                        self._agua_desligada=int(agua[0])
                else:
                    if dado:
                        self._record.append(int(dado_aux[0]))
                        self._dataHora.append(converte_data(dado_aux[1]+" "+dado_aux[2]))
                        self._peso.append(float(dado_aux[3]))

                        
                
    def retorna_dados(self):
        if self._opcao=="Intemperismo":
            dados={"record":self._record,
                "Data_Hora": self._dataHora,
                "temperatura(°C)":self._temperatura,
                "forca(kgf)":self._forca,
                "posição(mm)":self._posicao,
                "pH":self._ph,
                "Agua_ligada(min)":self._agua_ligada,
                "Agua_Desligada(min)":self._agua_desligada,
                "troca_agua":self._troca_agua,
                "Fonte_Energia":self._nobreak,
                }
        else:
            dados={"record":self._record,
                "Data_Hora": self._dataHora,
                "peso(g)":self._peso,
                }
        
        return dados

    def retornaXLS(self):
        df=pd.DataFrame(self.retorna_dados())
        buffer = BytesIO()
        file=df.to_excel(buffer,index=False)
        buffer.seek(0)

        return buffer
        

def geraXLS(file,opcao):
    dados_raw=file.read()
    dados_raw=boxplot.boxplot2.try_decode(dados_raw)
    dados=Dados(opcao)
    dados.carrega_dados(dados_raw)
    return dados.retornaXLS()
