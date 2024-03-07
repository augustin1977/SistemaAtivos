import pandas as pd
from io import BytesIO

class Converte_dados:
    def __init__(self,dados):
        self._raw_dados=dados
        self._dados={} # cria um dicionário
    def processa_dados(self):
        dados_linhas=self._raw_dados.split("\n")
        for linha in dados_linhas: # itera sobre as linhas
            if not linha: # se a linha estiver vazia pula
                pass
            elif linha[0]=='1': # caso o valor do primeiro caracter seja 1 inicia a leitura um novo horário
                cabecalho=linha.split("?")[1].split("^")[0]
                self._dados[cabecalho]={}# cria o novo dicionário do horário
            elif linha[0]=='2': # caso o valor do primeiro caracter seja 2 faz a leitura dos dados dentro do horário
                nome_valor=linha.split("?")[1].split("^") # Separa o nome da variavel do valor 
                if "." in nome_valor[1]: # verifica se o valor é um float, casdo contrario é um int
                    self._dados[cabecalho][nome_valor[0]]=float(nome_valor[1])
                else:
                    self._dados[cabecalho][nome_valor[0]]=int(nome_valor[1])
    def retornaXLS(self):
        df = pd.DataFrame(self._dados).T # transforma o dicionário num dataframe Pandas
        buffer = BytesIO()
        df.to_excel(buffer,index=False)
        buffer.seek(0)
        return buffer

def geraXLS(file):
    dados_raw=file.read()
    dados=Converte_dados(dados_raw)
    dados.processa_dados()

    
    return dados.retornaXLS()