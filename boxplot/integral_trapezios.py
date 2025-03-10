import re
import csv
from io import StringIO
def decodifica_Shimatsu(arquivo:StringIO) -> list[list[float]]:
    """Decodifica o arquivo csv da máquina 1

    Args:
        arquivo (StringIO): Recebe a referencia em memória de um arquivo csv proveniente da máquina 1

    Returns:
        list[list[float]]: retorna uma lista com os valores de força e deslocamento para cada aglomerado analisado
        sendo na primeira posição o tempo na segunda posição a força e na terceira posição o deslocamento
    """
    replace_comas=lambda match: match.group().replace(",",".")
    pattern = r'"\d+,\d+"'
    raw_data=arquivo.read().decode("ISO-8859-1") 
    # Substituir as vírgulas dentro dos números
    modified_csv = re.sub(pattern, replace_comas, raw_data)
    csv_reader = csv.reader(StringIO(modified_csv))
    data = []
    for row in csv_reader:
        new_row = []
        for id,value in enumerate(row):
            try:
                if id%3 ==1:
                    new_row.append(float(value)*10)  # Tenta converter para float e corrige unidade de kgf->N
                elif id%3==2:
                    new_row.append(float(value)/1000)  # Tenta converter para float e corrige unidade de mm->m
                else:
                    new_row.append(float(value)) # converte os demais valores    
            except ValueError:
                new_row.append(value)  # Mantém como string se não for número
        data.append(new_row)
    return data[4:]
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
        for id,value in enumerate(split_row):
            try:
                if id%3 ==1:
                    new_row[1]=(float(value)*1000)  
                elif id%3==2:
                    new_row[2]=(float(value)/1000)  # Tenta converter para float e corrige unidade de mm->m
                else:
                    new_row[0]=(float(value)) # converte os demais valores    
            except ValueError:
                new_row.append(value)  # Mantém como string se não for número
        data.append(new_row)
       
    return data
    

def calcula_energia(dados:list[list[float]])->float:
    """Calcula a energia de ruptura
    A energia de ruptura é calculada pela área sob a curva do gráfico de energia x tamanho de partícula
    A área é calculada pela soma dos trapézios formados pelos pontos do gráfico
    A área do trapézio é calculada pela média das alturas dos dois pontos adjacentes multiplicada pela base
    A base é a diferença entre os tamanhos de partícula dos dois pontos adjacentes
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
                energia[j+1]+=(dados[i][j*3+1]+dados[i-1][j*3+1])*(dados[i][j*3+2]-dados[i-1][j*3+2])/2
            except:
                pass
        
    return energia


