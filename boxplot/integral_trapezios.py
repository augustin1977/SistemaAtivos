import re
import csv
from io import StringIO
import matplotlib.pyplot as plt
import io
import matplotlib
import numpy as np  
import logging

def decodifica_Shimatsu(arquivo: StringIO) -> list[list[float]]:
    """Decodifica o arquivo csv da máquina 1

    Args:
        arquivo (StringIO): Recebe a referencia em memória de um arquivo csv proveniente da máquina 1

    Returns:
        list[list[float]]: Retorna uma matriz de valores numéricos processados
    """

    replace_comas = lambda match: match.group().replace(",", ".")
    pattern = r'"\d+,\d+"'  # Regex para encontrar números decimais entre aspas

    # Leitura do arquivo e substituição de vírgulas dentro de números
    raw_data = arquivo.read().decode("ISO-8859-1")
    modified_csv = re.sub(pattern, replace_comas, raw_data)
    
    csv_reader = csv.reader(StringIO(modified_csv), delimiter=",")  # Lendo CSV corretamente
    data = []

    for index, row in enumerate(csv_reader):
        if index < 3:  # Ignorar cabeçalhos e unidades (as 3 primeiras linhas)
            continue  

        new_row = []
        for id, value in enumerate(row):
            
            try:
                if id % 3 == 1:  # Coluna de Força (conversão para Newtons)
                    new_row.append(float(value) * 10)  
                    # logger.info(f"{id} {id//3} %3=1 - Foorça - {float(value) * 10}")      
                elif id % 3 == 2:  # Coluna de Deslocamento (conversão para metros)
                    new_row.append(float(value) / 1000) 
                    # logger.info(f"{id} {id//3} %3=2 - Deslocamento - {float(value) /1000}")     
                else:  # Tempo (ou outra métrica sem conversão)
                    new_row.append(float(value))
                    # logger.info(f"{id} {id//3} else - tempo - {float(value)}")   
            except ValueError:
                new_row.append(None)  # Evita erros caso a conversão falhe
                # logger.warning(f"{id} {id//3} - '{(value)}'") 

        # Adiciona a linha ao dataset apenas se houver valores numéricos relevantes

        data.append(new_row)
        # logger.info(f"linha {id} - {new_row}")
    return data
def decodifica_EMIC(arquivo:StringIO) -> list[list[float]]:
    """Decodifica o arquivo csv da máquina 2

    Args:
        arquivo (StringIO): Recebe a referencia em memória de um arquivo csv proveniente da máquina 1

    Returns:
        list[list[float]]: retorna uma lista com os valores de força e deslocamento para cada aglomerado analisado
        sendo na primeira posição o tempo na segunda posição a força e na terceira posição o deslocamento
    """
    raw_data=arquivo.read().decode("ISO-8859-1") 
    csv_reader = csv.reader(StringIO(raw_data))
    data = []
    for row in csv_reader:
        new_row = [0,0,0]
        for id,value in enumerate(row):
            try:
                if id%3 ==2:
                    new_row[1]=(float(value))  
                elif id%3==1:
                    new_row[2]=(float(value)/1000)  # Tenta converter para float e corrige unidade de mm->m
                else:
                    new_row[0]=(float(value)) # converte os demais valores    
            except ValueError:
                new_row.append(value)  # Mantém como string se não for número
        data.append(new_row)
       
    return data[1:]

def decodifica_MEC_ROCHAS(arquivo:StringIO) -> list[list[float]]:
    """Decodifica o arquivo csv da máquina 2

    Args:
        arquivo (StringIO): Recebe a referencia em memória de um arquivo csv proveniente da máquina 1

    Returns:
        list[list[float]]: retorna uma lista com os valores de força e deslocamento para cada aglomerado analisado
    """
    data_reader=arquivo.read().decode("ISO-8859-1") 
    data_reader=data_reader.replace(",",".")
    raw_data = data_reader.split("\n")   [21:]

    data = []
    for row in raw_data:
        new_row = [0,0,0]
        split_row=row.split("\t")
        if len(split_row)<3:
            continue
        for id,value in enumerate(split_row):
            try:
                if id%3 ==1:
                    new_row[1]=(float(value)*1000)  
                elif id%3==2:
                    new_row[2]=(float(value)/1000)  # Tenta converter para float e corrige unidade de mm->m
                else:
                    new_row[0]=(float(value)) # converte os demais valores    
            except ValueError:
                # new_row.append(value)  # Mantém como string se não for número
                pass
        data.append(new_row)
       
    return data[:-1]
    

def calcula_energia(dados:list[list[float]])->float:
    """Calcula a energia de ruptura
    A energia de ruptura é calculada pela área sob a curva do gráfico de energia x deslocamento
    A área é calculada pela soma dos trapézios formados pelos pontos do gráfico
    A área do trapézio é calculada pela média das alturas dos dois pontos adjacentes multiplicada pela base
    A base é o deslocamento de dois pontos adjacentes
    A energia é a soma das áreas dos trapézios
    Args:
        list[list[float | str]]: Recebe uma lista de listas com os dados do gráfico de força x deslocamento

    Returns:
        list[float,float]: retorna uma lista com os valores de energia de cada aglomerado calculado pelo metodo dos trapezios
    """
    energia={}

    for j in range(len(dados[0])//3):
        for i in range(1,len(dados)):
            try:
                if (j+1) not in energia:
                    energia[j+1]=0
                energia_calculdada=(dados[i][j*3+1]+dados[i-1][j*3+1])*(dados[i][j*3+2]-dados[i-1][j*3+2])/2
                # print(energia_calculdada)
                energia[j+1]+=energia_calculdada
                
            except Exception as e:
                pass
                
    return energia

def gerar_grafico_forca_deslocamento(dados, selecionados):
    if selecionados:
        dados_lista = [list(row) for row in dados]
        matplotlib.use("Agg")  # Modo não interativo
        plt.figure(figsize=(12, 9))
        colunas_selecionadas=[]
        for item in selecionados:
            colunas_selecionadas.append(int(item)-1)
        indice=[]
        for col_idx in map(int, colunas_selecionadas):
            forca=[]
            deslocamento=[]
            indice.append(col_idx+1)
            for row in dados_lista:
                if row[3*col_idx+1] not in ["", None] and row[3*col_idx+2] not in ["", None]:
                    forca.append( float(row[3*col_idx+1]))
                    deslocamento.append( float(row[3*col_idx+2]))

            plt.plot(deslocamento, forca, marker="+", linestyle="-", label=f"ID {item}")

        plt.xlabel("Deslocamento (m)")
        plt.ylabel("Força (N)")
        plt.title("Gráfico de Força x Deslocamento")
        plt.legend(labels=indice)
        plt.grid()
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        return buffer
    return None
