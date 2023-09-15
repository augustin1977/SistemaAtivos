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
            


def geraPlot(arquivo, comMedia):
    
    matplotlib.use('Agg')  # Modo não interativo
    # ------------- Convertendo dados--------------------
    
    
    dados=arquivo.read().decode('UTF-8')
    
       # ------------- ajustando preferencias--------------------
    # define tamanho dos textos
    tamanho_texto_super_pequeno="xx-small"
    tamanho_texto_pequeno="small"
    tamanho_texto_normal="large"
    tamanho_texto_grande="x-large"
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
    #print (tabela)
    titulo=tabela[0][0]
    # busca as familias dos ensaios na planilha
    familias = tabela[1]
    # busca atributos e segregando os dados
    eixoX=tabela[0][1]
    eixoY=tabela[0][2]
    nomes=tabela[2]
    dados_lidos=tabela[3:]
    #print(titulo)
    #print(eixoX)
    #print(eixoY)
    #print(nomes)
    #print(dados_lidos)
    # verificando se está tudo preenchido corretamente
    dados_verificados=[]
    contagem_colunas=[0]*len(nomes)
    for l,linha in enumerate(dados_lidos):
        if len(linha)==len(nomes):
            nova_linha=[]
            for c,dado in enumerate(linha):
                try: 
                    nova_linha.append(float(dado))
                    contagem_colunas[c]+=1
                except:
                    dados_lidos[l][c]=False
            dados_verificados.append(nova_linha)
    dados_verificados=transpoe_matriz(dados_verificados)
    media=[0]*len(dados_verificados)
    for n in range(len(media)):
        media[n]=sum(dados_verificados[n])/len(dados_verificados[n])
    #print(dados_verificados)  
    #print(media)    
    cols=0
    for i in nomes:
        if (i!=""):
            cols+=1
    if (cols>20):
        tamanho_texto=tamanho_texto_super_pequeno
    elif (cols>10):
        tamanho_texto=tamanho_texto_pequeno
    else:
        tamanho_texto=tamanho_texto_normal

    #cria biblioteca de cores
    corGrafico={}
    j=0;
    for i in familias:
        if i not in corGrafico:
            if (str(i).upper()=="REFERENCIA"or str(i).upper()=="REFERÊNCIA" or str(i).upper()=="REF" or str(i).upper()=="REFERENCE"):
                numero_linha_media_referencia=j
                corGrafico[i]='red'
            else:
                corGrafico[i]=cor[j];
            j=j+1



   
    # # criando area de plotagem e definindo variaves globais como nome do grafico
    
    fig1, ax1 = plt.subplots(figsize=(12,len(nomes)))
    #print(len(nomes), len(dados_verificados[0]))
    if (len(nomes)==len(dados_verificados)):
        #print("Numero de nomes:",len(nomes))
        #print("numero de dados:",len(dados_verificados))

        # cria propriedades da linha de media e da mediana
        propriedades_medianas={'color':vermelho,'linewidth':1.5}
        propriedades_medias={"linestyle":"-","color":verde}
        # cria boxplot mostrando medias e linha de medias(showmean e meanline True) com dados na vertical (vert=False) sem outliers(showfliers=False) 
        #graf=ax1.boxplot(dataset,labels=nomes,vert=False,showmeans=True,meanline=True,medianprops=propriedades_medianas,meanprops=propriedades_medias,flierprops={"marker":"+"},patch_artist=True,showfliers=False)

        # cria boxplot mostrando medias e linha de medias(showmean e meanline True) com dados na vertical (vert=False) com outliers
        graf=ax1.boxplot(dados_verificados,labels=nomes,vert=False,showmeans=True,meanline=True,medianprops=propriedades_medianas,meanprops=propriedades_medias,flierprops={"marker":"+"},patch_artist=True)
       
        
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
        ax1.set_title(titulo, fontsize=tamanho_texto_grande,fontweight="bold")
        ax1.set_xlabel(eixoX,fontsize=tamanho_texto_normal,fontweight="bold")
        ax1.set_ylabel(eixoY,fontsize=tamanho_texto_normal,fontweight="bold")

        #ajustes de posições para melhor enquadramento
        #fig1.subplots_adjust(left=0.17,right=0.98,top=0.96,bottom=0.07)
        fig1.tight_layout()
        # Faz a linha media do ensaio de referencia  se comMedia=True(ultimo)
        #print(comMedia)
        if comMedia:
            ax1.axvline(media[numero_linha_media_referencia], ymin=0, ymax=len(media),linewidth=1, color=verde,linestyle=':')

        # exibe linha de grade
        #ax1.yaxis.grid(True)
        #ax1.xaxis.grid(True)

        # pinta cada boxplot com a cor de sua familia
        legenda=[] 
        # cria legenda já com suas cores
        for patch, color in zip(graf['boxes'], familias):  
            patch.set_facecolor(corGrafico[color])
            legenda.append(mpatches.Patch(color=corGrafico[color], label=color))


        #constroi a legenda
        ax1.legend(handles=legenda).set_draggable(True)
        # mostra o grafico
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        #print("retornando buffer")
        return buffer
    else:
        #print("Deu erro")
        return False

