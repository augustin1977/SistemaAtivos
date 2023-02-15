def retiraespacos(palavra):
    resultado=""
    for letra in palavra:
        if not letra==" ":
            resultado+=letra.upper()
    return resultado
            
def fazlista(palavra,lista): # precisa arrumar pra migrar certinho
    letras="ABCDEFGHIJKLMOPQRSTUVXYWZ"
    siglas=[]
    for palavra in lista:
        item=retiraespacos(palavra)
        i=0
        j=i+1
        k=j+1
        sigla=item[i].upper()+item[j].upper()+item[k].upper()
        while(sigla in siglas and i<len(item)):
            while(sigla in siglas and j<len(item)):
                while(sigla in siglas and k<len(item)):

                    
                    sigla=item[i].upper()+item[j].upper()+item[k].upper()
                    print(i,j,k,sigla,item)
                    k+=1
                j+=1
            i+=1
        if i==j and j==k and k==len(item):
            i=0
            while(sigla in siglas and i<len(letras)):
                sigla=sigla[:-1]+letras[i]
                print(sigla,i)
                i+=1
            if i==len(letras):
                sigla='XXX'
        siglas.append(sigla)
        siglas.sort()
    return siglas