import random

def retiraespacos(palavra):
    """Recebe um string e retorna esse string sem espaços ou caracteres não imprimiveis"""
    resultado=""
    for letra in palavra:
        if not letra==" ":
            resultado+=letra.upper()
    return resultado
            
def fazlista(palavra,lista):
    """Recebe um string e uma lista de string e retorna uma string de 3 caracteres,
      que possuo o maior numeros de caracteres da string original e que não esteja contida na lista """
    letras="ABCDEFGHIJKLMOPQRSTUVXYWZ"
    siglas=lista
    item=retiraespacos(palavra)
    if len(item)>=3:
        i=0
        j=i+1
        k=j+1
        sigla=item[i].upper()+item[j].upper()+item[k].upper()
        while(sigla in siglas and i<len(item)):
            while(sigla in siglas and j<len(item)):
                while(sigla in siglas and k<len(item)):
                    sigla=item[i].upper()+item[j].upper()+item[k].upper()
                    k+=1
                j+=1
            i+=1
        if i==j and j==k and k==len(item):
            i=0
            while(sigla in siglas and i<len(letras)):
                sigla=sigla[:-1]+letras[i]
                i+=1
            if i==len(letras):
                sigla='XXX'
        
    elif len(item)>0:
        while(sigla in siglas and i<len(letras)):
                sigla=sigla[1]+letras[i]+letras[(random.randint(0,len(letras)))]
                i+=1
    else:
        sigla="XXX"
    siglas.append(sigla)
       
    return sigla