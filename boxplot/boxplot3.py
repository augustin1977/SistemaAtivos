import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from io import BytesIO
import matplotlib
import matplotlib.colors as mcolors
from statistics import stdev,mean

tamanho_texto_super_pequeno = "xx-small"
tamanho_texto_pequeno = "small"
tamanho_texto_normal = "large"
tamanho_texto_grande = "x-large"
tamanho_texto_super_grande = "xx-large"
verde = "#008000"
# define vermelho da mediana
vermelho = "#950070"
# cria lista de cores
cores= ["yellow",
        "orange",
        "pink",
        "lightgreen",
        "lightseagreen",
        "deepskyblue",
        "cyan",
        "lightblue",
        "blue",
        "darkblue",
        "slateblue",
        "darkviolet",
        "magenta",
        "violet",
        "purple",
        "brown",
        "silver",
        "gray",
        "black",
        "olive", 
        "goldenrod",
        "beige", 
        ]


def exclui_sem_none_e_repetidos(colunas):
    novascolunas=[]
    for coluna in colunas:
        if coluna!="" and coluna not in novascolunas:
            novascolunas.append(coluna)
    # continua = True
    # while continua:
    #     if colunas[-1] == "":
    #         colunas.pop(-1)
    #     else:
    #         continua = False
    
    return novascolunas


def try_decode(
    text,
    encodings=[
        "utf-8",
        "iso-8859-1",
        "windows-1252",
        "CP850",
        "iso-8859-15 ",
        "MacRoman",
    ],
):
    for encoding in encodings:
        try:
            decoded_text = text.decode(encoding)
            return decoded_text
        except UnicodeDecodeError:
            pass
    # Se nenhuma codificação funcionou, retorne None ou levante uma exceção, dependendo do seu caso.
    return None  # Ou raise Exception("Nenhuma codificação válida encontrada")


def colocareferencianofim(matriz):
    # trocaposição de todos os elementos
    tam = len(matriz)
    for i in range(tam // 2):
        # inverte a matriz
        temp = matriz[i]
        matriz[i] = matriz[tam - i - 1]
        matriz[tam - i - 1] = temp
    return matriz



class Boxplot:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.dados_raw = None
        self.dados=[]
        self.ensaios = []
        self.familias=[]
        self.graficos=[]
        self.familias_graficos=[]
        self.medias = []
        self.DP=[]
        self.CV=[]
        self.maximo=[]

    def le_dados(self):
        """Lê os dados do arquivo csv """
        if not self.arquivo:
            self.erro=1 # Sem arquivo
        self.dados_raw = self.arquivo.read()
        self.dados_raw = try_decode(self.dados_raw)
        if self.dados_raw == None:
            self.erro=3 # impossivel decodificar
    
    def organiza_dados(self):
        tabela = []
        linhas = self.dados_raw.split("\n")
        for linha in linhas:
            l = linha.split("\r")
            tabela.append(l[0].split(";"))
        
        self.titulo = tabela[0][0]
        self.graficos = exclui_sem_none_e_repetidos(tabela[1])
        self.familias = exclui_sem_none_e_repetidos(tabela[2])
        self.ensaios = exclui_sem_none_e_repetidos(tabela[3])
        self.eixox = tabela[0][1]
        self.eixoy = tabela[0][2]
        
        dados_lidos = tabela[1:]
        dados_parametrizados = []
        for linha in range(len(dados_lidos)):
            for coluna in range(len(tabela[3])):
                try:
                    dado = dados_lidos[linha][coluna].replace(",", ".")
                except:
                    pass
                if linha == 0:
                    try:
                        dados_parametrizados.append([float(dado)])
                    except:
                        if dado != "":
                            dados_parametrizados.append([dado])
                else:
                    try:
                        dados_parametrizados[coluna].append(float(dado))
                    except:
                        if dado != "":
                            dados_parametrizados[coluna].append(dado)

        self.dados = []
        vazio=self.familias[-1]

        # Preenche gráficos com as categorias sem dados com listas vazias
        # print (dados_parametrizados)
        for grafico in self.graficos:
            
            camada=[]
            camada_grafico=[]
            medias=[]
            dps=[]
            cvs=[]
            maximo=[]
            for ensaio in self.ensaios:
                nao_preencheu=True
                for coluna in dados_parametrizados:   
                    if coluna[0]==grafico and coluna[2]==ensaio:
                        camada.append(coluna[3:])
                        camada_grafico.append(coluna[1])
                        m=mean(coluna[3:])
                        dp=stdev((coluna[3:])) 
                        cv=100*abs(dp/m) if m != 0 else float('inf')
                        medias.append(m)
                        dps.append(dp)
                        cvs.append(cv)
                        maximo.append(max(coluna[3:]))
                        
                        nao_preencheu=False
                if nao_preencheu:
                    nao_preencheu=False
                    camada.append([])
                    medias.append("")
                    dps.append("")
                    cvs.append("")
                    maximo.append("")
                    camada_grafico.append(vazio)
                   
            self.dados.append(camada[::-1])
            self.familias_graficos.append(camada_grafico[::-1])
            self.medias.append(medias[::-1])
            self.DP.append(dps[::-1])
            self.CV.append(cvs[::-1])
            self.maximo.append(maximo[::-1])
        self.ensaios=self.ensaios[::-1]
        self.familias=self.familias[::-1]


    def gera_grafico(self, linha_media, valor_media, CV, labelcores, legenda):
        matplotlib.use("Agg")
        maxnomes = len(max(self.ensaios, key=lambda x: len(x)))
        x = max((maxnomes) // 8 + len(self.ensaios) // 3+ 2 * len(self.graficos), 12)
        y = max(6 + len(self.ensaios) // 4, 8)

        tamanho_texto = tamanho_texto_grande if (x > 12 and y > 8) else tamanho_texto_normal
        fig1, ax1 = plt.subplots(nrows=1, ncols=len(self.graficos), figsize=(x, y))

        # Criação do dicionário para associar cores às famílias
        
        

        propriedades_medianas = {"color": vermelho, "linewidth": 1.5}
        propriedades_medias = {"linestyle": "-", "color": verde}

        for i, grafico in enumerate(self.graficos):
            # print(f"Dados do gráfico {grafico}: {self.dados[i]}")
            # print(f"Familia_graficos {self.familias_graficos}")
            # print(f"Medias {self.medias[i]}")
            # print()
            corGrafico = {}
            j = 0
            for familia in self.familias:
                # print(familia)
                if familia.lower() in ["referencia", "referência", "ref", "reference", "ref."]:
                    corGrafico[familia] = "red"  # Referência sempre vermelha
                else:
                    corGrafico[familia] = cores[j % len(cores)]  # Pegando cor da lista 'cores'
                    j += 1
            # Inicializar a lista de dados completos com listas vazias para cada ensaio
            

            # Desenhar o boxplot para o gráfico atual com cores da família
            if i==0:
                graf = ax1[i].boxplot(
                self.dados[i],
                labels=self.ensaios,
                vert=False,
                showmeans=True,
                meanline=True,
                medianprops=propriedades_medianas,
                meanprops=propriedades_medias,
                flierprops={"marker": "+"},
                patch_artist=True,
                )  
            else:
                graf = ax1[i].boxplot(
                self.dados[i],
                labels=[""]*len(self.ensaios),
                vert=False,
                showmeans=True,
                meanline=True,
                medianprops=propriedades_medianas,
                meanprops=propriedades_medias,
                flierprops={"marker": "+"},
                patch_artist=True,
                )  
                 
            if labelcores:
                for label, familia in zip(ax1[i].get_yticklabels(), self.familias_graficos[i]):
                    if (
                        familia.lower() == "referencia"
                        or familia.lower() == "referência"
                        or familia.lower() == "ref"
                        or familia.lower() == "reference"
                        or familia.lower() == "ref."
                    ):
                        label.set_color("red")
                    else:
                        label.set_color("black")
            
            
            
            
            # Ajuste: mapear cores usando tanto a familia quanto o ensaio
            for patch, (familia, ensaio) in zip(graf['boxes'], zip(self.familias_graficos[i], self.ensaios)):
                patch.set_facecolor(corGrafico[familia])

            ax1[i].set_title(grafico, fontsize=tamanho_texto_super_grande, fontweight="bold")
            ax1[i].set_xlabel(self.eixox, fontsize=tamanho_texto, fontweight="bold")

            # Adicionar legenda ao primeiro gráfico (i == 0)
            if i == 0 :
                patches = [mpatches.Patch(color=corGrafico[familia], label=familia) for familia in self.familias]
                
                patches.reverse()
                # constroi a legenda
                if not(legenda=="NA"): # Se a posição foi diferente de NA
                    ax1[i].legend(handles=patches, loc=int(legenda), fontsize=tamanho_texto_pequeno)
                
                
                ax1[i].set_ylabel(self.eixoy, fontsize=tamanho_texto, fontweight="bold")    
            if linha_media:
                for j, familia in enumerate(self.familias_graficos[i]):
                    if (
                        familia.lower() == "referencia"
                        or familia.lower() == "referência"
                        or familia.lower() == "ref"
                        or familia.lower() == "reference"
                        or familia.lower() == "ref."
                    ):
                        ax1[i].axvline(
                            self.medias[i][j],
                            ymin=0,
                            ymax=len(self.dados[i][j]),
                            linewidth=1,
                            color=verde,
                            linestyle=":",
                        )
            if len(self.medias[i]) < 3:
                offset = 1.1
            elif len(self.medias[i]) < 4:
                offset = 1.2
            else:
                offset = 1.3
            for j in range(len(self.medias[i])):
            # Coloca valor do coeficiente de variação e media no boxplot
  
                if(CV):
                    if not (self.maximo[i][j]==""):
                        posx=self.maximo[i][j]
                    else: 
                        posx=0
                    try:
                        ax1[i].text(posx,j + offset-0.40,
                        "CV:{:.2f}%".format(self.CV[i][j]),
                        size=tamanho_texto,
                        color="black",
                        horizontalalignment="left", alpha=0.5
                            )
                    except:
                        pass # Se der erro não faz nada 
                # Coloca um texto com o valor da média de cada coluna no grafico
                if (valor_media):
                    try:
                        
                        if abs(self.medias[i][j]) > 1000000:
                            ax1[i].text(self.medias[i][j],j + offset,
                                "{:.0f}".format(self.medias[i][j]),
                                size=tamanho_texto,
                                color=verde,
                                horizontalalignment="center",
                            )
                            
                        elif abs(self.medias[i][j]) > 1000:
                            ax1[i].text(
                                self.medias[i][j],
                                j + offset,
                                "{:.1f}".format(self.medias[i][j]),
                                size=tamanho_texto,
                                color=verde,
                                horizontalalignment="center",
                            )
                            
                        elif abs(self.medias[i][j]) > 50:
                            ax1[i].text(
                                self.medias[i][j],
                                j + offset,
                                "{:.2f}".format(self.medias[i][j]),
                                size=tamanho_texto,
                                color=verde,
                                horizontalalignment="center",
                            )
                            
                        elif abs(self.medias[i][j]) > 1:
                            ax1[i].text(
                                self.medias[i][j],
                                j + offset,
                                "{:.3f}".format(self.medias[i][j]),
                                size=tamanho_texto,
                                color=verde,
                                horizontalalignment="center",
                            )
                        elif abs(self.medias[i][j]) > 0.1:
                            ax1[i].text(
                                self.medias[i][j],
                                j + offset,
                                "{:.4f}".format(self.medias[i][j]),
                                size=tamanho_texto,
                                color=verde,
                                horizontalalignment="center",
                            )
                        elif abs(self.medias[i][j]) > 0.001:
                            ax1[i].text(
                                self.medias[i][j],
                                j + offset,
                                "{:.6f}".format(self.medias[i][j]),
                                size=tamanho_texto,
                                color=verde,
                                horizontalalignment="center",
                            )    
                        else:
                            ax1[i].text(
                                self.medias[i][j],
                                j + offset,
                                "{}".format(self.medias[i][j]),
                                size=tamanho_texto,
                                color=verde,
                                horizontalalignment="center",
                            )
                    except:
                        pass # Se de rerro Não faz anda e não escreve a media
                        
                        
            
        fig1.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        return buffer
        pass



def gera_boxplot(arquivo, linha_media, valor_media, CV, labelcores, legenda):
    boxplot = Boxplot(arquivo)
    boxplot.le_dados()
    boxplot.organiza_dados()
    grafico = boxplot.gera_grafico(linha_media, valor_media, CV, labelcores, legenda)
    return grafico
