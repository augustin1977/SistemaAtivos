import random
import datetime

def formatar_data_por_extenso(data):
    meses = {
        1: 'janeiro',
        2: 'fevereiro',
        3: 'março',
        4: 'abril',
        5: 'maio',
        6: 'junho',
        7: 'julho',
        8: 'agosto',
        9: 'setembro',
        10: 'outubro',
        11: 'novembro',
        12: 'dezembro'
    }

    dia = data.day
    mes_numero = data.month
    mes_extenso = meses[mes_numero]
    ano = data.year

    data_por_extenso = f"{dia} de {mes_extenso} de {ano}"
    return data_por_extenso

def retiraespacos(palavra):
    """Recebe um string e retorna esse string sem espaços ou caracteres não imprimiveis"""
    resultado = ""
    for letra in palavra:
        if not letra == " ":
            resultado += letra.upper()
    return resultado


def fazlista(palavra, lista):
    """Recebe um string e uma lista de string e retorna uma string de 3 caracteres,
    que possuo o maior numeros de caracteres da string original e que não esteja contida na lista
    """
    letras = "ABCDEFGHIJKLMOPQRSTUVXYWZ"
    siglas = lista
    item = retiraespacos(palavra)
    if len(item) >= 3:
        i = 0
        j = i + 1
        k = j + 1
        sigla = item[i].upper() + item[j].upper() + item[k].upper()
        while sigla in siglas and i < len(item):
            while sigla in siglas and j < len(item):
                while sigla in siglas and k < len(item):
                    sigla = item[i].upper() + item[j].upper() + item[k].upper()
                    k += 1
                j += 1
            i += 1
        if i == j and j == k and k == len(item):
            i = 0
            while sigla in siglas and i < len(letras):
                sigla = sigla[:-1] + letras[i]
                i += 1
            if i == len(letras):
                sigla = "XXX"

    elif len(item) > 0:
        while sigla in siglas and i < len(letras):
            sigla = sigla[1] + letras[i] + letras[(random.randint(0, len(letras)))]
            i += 1
    else:
        sigla = "XXX"
    siglas.append(sigla)

    return sigla
