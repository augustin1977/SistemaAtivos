import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from io import BytesIO
import matplotlib

#----------------funções auxiliares ------------------
def transpoe_matriz(matriz):
    novamatriz=[]
    for i in range(len(matriz[0])):
        novalinha=[]
        for j in range(len(matriz)):
            try:
                novalinha.append(matriz[j][i])
            except:
                pass
        novamatriz.append(novalinha)
    return novamatriz

def try_decode(text, encodings=['utf-8', 'iso-8859-1','windows-1252', 'CP850','iso-8859-15 ', 'MacRoman']):
    
    
    for encoding in encodings:
        try:
            decoded_text = text.decode(encoding)
            return decoded_text
        except UnicodeDecodeError:
            pass
    # Se nenhuma codificação funcionou, retorne None ou levante uma exceção, dependendo do seu caso.
    return None  # Ou raise Exception("Nenhuma codificação válida encontrada")

  
def colocareferencianofim(matriz,familias,media,nomes):
    # trocaposição de todos os elementos
    tam=len(familias)
    for i in range(tam//2):
        #inverte a matriz
        temp=matriz[i]
        matriz[i]=matriz[tam-i-1]
        matriz[tam-i-1]=temp
        #inverte a familia
        temp=familias[i]
        familias[i]=familias[tam-i-1]
        familias[tam-i-1]=temp
        #inverte a media
        temp=media[i]
        media[i]=media[tam-i-1]
        media[tam-i-1]=temp
        #inverte os nomes
        temp=nomes[i]
        nomes[i]=nomes[tam-i-1]
        nomes[tam-i-1]=temp
        
    # caso a referencia não seja a ultima troca 
    temp5=tam-1
    
    # for n,familia in enumerate(familias):
    #     if (familia.upper()=="REFERENCIA" or 
    #             familia.upper()=="REFERÊNCIA" or 
    #             familia.upper()=="REF" or 
    #             familia.upper()=="REFERENCE" or
    #             familia.upper()=="REF." ):
    #         temp1=familias.pop(n)
    #         temp2=matriz.pop(n)
    #         temp3=media.pop(n)
    #         temp4=nomes.pop(n)
    #         temp5=n
    #         familias.append(temp1)
    #         matriz.append(temp2)
    #         media.append(temp3)
    #         nomes.append(temp4)
    return matriz,familias,media,nomes,temp5

def geraPlot(arquivo, comMedia,labelcores):
    
    matplotlib.use('Agg')  # Modo não interativo
    # ------------- Convertendo dados--------------------
    
    if not arquivo:
        return False
    dados = arquivo.read()
    dados= try_decode(dados)
    if dados==None:
        return 3 # erro de decodificação do documento
    
       # ------------- ajustando preferencias--------------------
    # print(dados)
    # define tamanho dos textos
    tamanho_texto_super_pequeno="xx-small"
    tamanho_texto_pequeno="small"
    tamanho_texto_normal="large"
    tamanho_texto_grande="x-large"
    tamanho_texto_super_grande="xx-large"
    # define Verde da média
    verde="#008000"
    #define vermelho da mediana
    vermelho='#950070'
    # cria lista de cores 
    cor=['yellow','orange','pink','lightgreen','green','lightblue','blue','purple', 'brown','gray','black']
    #cor=['yellow','pink','lightblue','red','gray', 'brown','lightgreen','black','purple']
 

    # ------------- Programa--------------------
    # puxando dados do arquivo
    tabela=[]
    linhas=dados.split("\n")
    for linha in linhas:
        l=linha.split("\r")
        tabela.append(l[0].split(";")) 
    # print (tabela)
    titulo=tabela[0][0]
    # busca as familias dos ensaios na planilha
    familias = tabela[1]
    # busca atributos e segregando os dados
    eixoX=tabela[0][1]
    eixoY=tabela[0][2]
    nomes=tabela[2]
    dados_lidos=tabela[3:]

    dados_verificados=[]
    contagem_colunas=[0]*len(nomes)
    
    for l,linha in enumerate(dados_lidos):
        nova_linha=[]
        for c,dado in enumerate(linha):
            try: 
                dado=dado.replace(",",".")
                nova_linha.append(float(dado))
                contagem_colunas[c]+=1
            except:
                dados_lidos[l][c]=False
        dados_verificados.append(nova_linha)
    # print(dados_verificados)
    dados_verificados=transpoe_matriz(dados_verificados)
    media=[0]*len(dados_verificados)
    for n in range(len(media)):
        media[n]=sum(dados_verificados[n])/len(dados_verificados[n])
    # print(dados_verificados)  
    # print(media)    
    cols=0
    # print(nomes)
    for i in nomes:
        if (i!=""):
            cols+=1
    if (cols>20):
        tamanho_texto=tamanho_texto_pequeno
    elif (cols>10):
        tamanho_texto=tamanho_texto_pequeno
    else:
        tamanho_texto=tamanho_texto_normal

    #cria biblioteca de cores
    

    # # criando area de plotagem e definindo variaves globais como nome do grafico
    
    fig1, ax1 = plt.subplots(figsize=((10+len(nomes))//2,5+len(nomes)//4))
    # print(len(nomes), len(dados_verificados))
    if (len(nomes)==len(dados_verificados)):

        # coloca a referencia no final
        dados_verificados,familias,media,nomes,numero_linha_media_referencia=colocareferencianofim(dados_verificados,familias,media,nomes)
        # ajusta legenda e cores dos graficos
        # print(dados_verificados)
        corGrafico={}
        j=0;
        for i,familia in enumerate(familias):
            if familia not in corGrafico:
                #if i==numero_linha_media_referencia:
                if familia.lower()=="referencia" or familia.lower()=="referência" or familia.lower()=="ref" or familia.lower()=="reference" or familia.lower()=="ref.":
                    corGrafico[familia]='red'
                else:
                    corGrafico[familia]=cor[j];
                j=j+1
        

        # cria propriedades da linha de media e da mediana
        propriedades_medianas={'color':vermelho,'linewidth':1.5}
        propriedades_medias={"linestyle":"-","color":verde}
      
        # cria boxplot mostrando medias e linha de medias(showmean e meanline True) com dados na vertical (vert=False) com outliers
        graf=ax1.boxplot(dados_verificados,labels=nomes,vert=False,showmeans=True,meanline=True,medianprops=propriedades_medianas,meanprops=propriedades_medias,flierprops={"marker":"+"},patch_artist=True)
        # Coloca label vermelho na familia referencia
        if labelcores:
            for label,familia in zip(ax1.get_yticklabels(),familias):
                if familia.lower()=="referencia" or familia.lower()=="referência" or familia.lower()=="ref" or familia.lower()=="reference" or familia.lower()=="ref.":
                    label.set_color("red")
                else:
                    label.set_color('black')
        # Coloca um texto com o valor da média de cada coluna no grafico
        if len(media)<3:
            offset=1.1
        elif len(media)<4:
            offset=1.2
        else:
            offset=1.3
        for i in range(len(media)):
            if media[i]>1000000:
                ax1.text(media[i],i+offset,"{:d}".format(media[i]),size=tamanho_texto,color=verde,horizontalalignment ='center')
            elif media [i]>1000:
                ax1.text(media[i],i+offset,"{:.1f}".format(media[i]),size=tamanho_texto,color=verde,horizontalalignment ='center')
            elif media [i]>1:
                ax1.text(media[i],i+offset,"{:.2f}".format(media[i]),size=tamanho_texto,color=verde,horizontalalignment ='center')
            elif media [i]>0.0001:
                ax1.text(media[i],i+offset,"{:.4f}".format(media[i]),size=tamanho_texto,color=verde,horizontalalignment ='center')
            else:
                ax1.text(media[i],i+offset,"{}".format(media[i]),size=tamanho_texto,color=verde,horizontalalignment ='center')
            
        # define titulo do grafico e dos eixos
        if cols>20:
            ax1.set_title(titulo, fontsize=tamanho_texto_super_grande,fontweight="bold")
            ax1.set_xlabel(eixoX,fontsize=tamanho_texto_grande,fontweight="bold")
            ax1.set_ylabel(eixoY,fontsize=tamanho_texto_grande,fontweight="bold")
        elif len(titulo)>25:
            ax1.set_title(titulo, fontsize=tamanho_texto_normal,fontweight="bold")
            ax1.set_xlabel(eixoX,fontsize=tamanho_texto_normal,fontweight="bold")
            ax1.set_ylabel(eixoY,fontsize=tamanho_texto_normal,fontweight="bold")
        else:
            ax1.set_title(titulo, fontsize=tamanho_texto_grande,fontweight="bold")
            ax1.set_xlabel(eixoX,fontsize=tamanho_texto_normal,fontweight="bold")
            ax1.set_ylabel(eixoY,fontsize=tamanho_texto_normal,fontweight="bold")

        #ajustes de posições para melhor enquadramento
        #fig1.subplots_adjust(left=0.17,right=0.98,top=0.96,bottom=0.07)
        fig1.tight_layout()
        # Faz a linha media do ensaio de referencia  se comMedia=True(ultimo)
        #print(comMedia)
        if comMedia:
            for i,familia in enumerate(familias):
                if familia.lower()=="referencia" or familia.lower()=="referência" or familia.lower()=="ref" or familia.lower()=="reference" or familia.lower()=="ref.":
                    ax1.axvline(media[i], ymin=0, ymax=len(media),linewidth=1, color=verde,linestyle=':')

        # pinta cada boxplot com a cor de sua familia
        legenda=[]
        incluido=[] 
        # cria legenda já com suas cores
        for patch, color in zip(graf['boxes'], familias):  
            patch.set_facecolor(corGrafico[color])
            if color not in incluido:
                incluido.append(color)
                legenda.append(mpatches.Patch(color=corGrafico[color], label=color))
        legenda.reverse()
        #constroi a legenda
        ax1.legend(handles=legenda).set_draggable(True)
        # mostra o grafico
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        #print("retornando buffer")
        return buffer
    else:
        return False

