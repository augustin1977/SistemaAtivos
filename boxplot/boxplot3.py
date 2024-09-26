import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from io import BytesIO
import matplotlib
import matplotlib.colors as mcolors
from statistics import median,stdev
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


    
def exclui_sem_none(colunas):
    continua = True
    while continua:
        if colunas[-1] == "":
            colunas.pop(-1)
        else:
            continua = False
    return colunas


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


class Boxplot():
    def __init__(self,arquivo):
        """Define variaveis da classe e inicializa todas elas com valores iniciais"""
        self.arquivo=arquivo
        self.dados=[]
        self.dados_verificados=[]
        self.familias=[]
        self.nomes=[]
        self.contagem_colunas=0
        self.eixox=""
        self.eixoy=""
        self.titulo=""
        self.medias=[]
        self.maximo=[]
        self.CV=[]
        self.DP=[]
        self.erro=0
        
    def status(self):
        return (self.erro==0)
    def le_dados(self):
        if not self.arquivo:
            self.erro=1 # Sem arquivo
        self.dados = self.arquivo.read()
        self.dados = try_decode(self.dados)
        if self.dados == None:
            self.erro=3 # impossivel decodificar
    def limpa_dados(self):
        tabela = []
        linhas = self.dados.split("\n")
        for linha in linhas:
            l = linha.split("\r")
            tabela.append(l[0].split(";"))
        print (tabela)
        self.titulo = tabela[0][0]
        # busca as familias dos ensaios na planilha
        self.familias = exclui_sem_none(tabela[1])
        # busca atributos e segregando os dados
        self.eixox = tabela[0][1]
        self.eixoy = tabela[0][2]
        self.nomes=exclui_sem_none(tabela[2])
        print(self.titulo,self.familias,self.eixox,self.eixoy,self.nomes)
        dados_lidos = tabela[3:]
        self.contagem_colunas = len(self.nomes)
        print(dados_lidos)
        for linha in range(len(dados_lidos)):
            for coluna in range(len(self.nomes)):
                try:
                    dado = dados_lidos[linha][coluna].replace(",", ".")
                    if linha==0:
                        self.dados_verificados.append([float(dado)])
                    else:
                        self.dados_verificados[coluna].append(float(dado))
                except:
                    pass
        print(self.dados_verificados)

    def calcula_medias(self):
        tam=len(self.dados_verificados)
        self.medias = [0] * tam
        self.DP=[0] * tam
        self.CV=[0] * tam
        self.maximo= [float('-inf')] * tam
        for n,dados in enumerate(self.dados_verificados):
            if not dados:
                raise ValueError("Foi encontrada coluna vazia no arquivo, favor corrigir")
            self.medias[n] = sum(dados) / len(dados)
            self.DP[n] = stdev(dados)
            self.CV[n] = abs(self.DP[n]/ self.medias[n] ) * 100 if self.medias[n] != 0 else float('inf')  # Lida com média zero
            self.maximo[n]=max(dados)
        
        
        # for n in range(tam):
        #     if not self.dados_verificados[n]:
        #         raise ValueError(f"Sublista vazia encontrada na posição {n}")
        #     self.medias[n] = sum(self.dados_verificados[n]) / len(self.dados_verificados[n])
        #     self.DP[n] = stdev(self.dados_verificados[n])
        #     self.CV[n] = abs(self.DP[n]/ self.medias[n] * 100) if self.medias[n] != 0 else float('inf')  # Lida com média zero
        #     self.maximo[n]=max(self.dados_verificados[n])
            
            

    def organiza_dados(self):
        if len(self.nomes)==len(self.dados_verificados):
            self.dados_verificados=colocareferencianofim(self.dados_verificados)
            self.familias=colocareferencianofim(self.familias)
            self.medias=colocareferencianofim(self.medias)
            self.nomes=colocareferencianofim(self.nomes)
            self.maximo=colocareferencianofim(self.maximo)
            self.CV=colocareferencianofim(self.CV)
            self.DP=colocareferencianofim(self.DP)
        else:
            self.erro=2 # Erro - numero de nomes diferentes do numero de coluna de dados
        
        
    def gera_grafico(self,linha_media,valor_media,cv,labelcores,posicao_legenda):
        if self.erro==0:
            matplotlib.use("Agg")  # Modo não interativo
            maxnomes = len(max(self.nomes, key=lambda x: len(x))) # tamanho do maior nome de categoria
            
            x=max((maxnomes) // 8 + self.contagem_colunas // 3, 12)
            y=max(6+self.contagem_colunas // 4, 8)
            
            # Define o tamnaho do texto do gráfico
            if (x>12 and y> 8):
                tamanho_texto = tamanho_texto_grande
                tamanho_texto_eixo=tamanho_texto_grande
            else:
                tamanho_texto = tamanho_texto_normal
                tamanho_texto_eixo=tamanho_texto_normal
            
            
            fig1, ax1 = plt.subplots( figsize=(x, y)) # define o tamanho do grafico
            # definindo a cor das familias no boxplot
            corGrafico = {}
            j = 0
            for familia in reversed(self.familias):
                if familia not in corGrafico:
                    # if i==numero_linha_media_referencia:
                    if (    familia.lower() == "referencia"
                            or familia.lower() == "referência"
                            or familia.lower() == "ref"
                            or familia.lower() == "reference"
                            or familia.lower() == "ref." ):
                        corGrafico[familia] = "red"  
                    else:

                        corGrafico[familia] = cores[(j)%len(cores)]
                        j = j + 1

            # cria propriedades da linha de media e da mediana
            propriedades_medianas = {"color": vermelho, "linewidth": 1.5}
            propriedades_medias = {"linestyle": "-", "color": verde}

            # cria boxplot mostrando medias e linha de medias(showmean e meanline True) com dados na vertical (vert=False) com outliers
            graf = ax1.boxplot(
                self.dados_verificados,
                labels=self.nomes,
                vert=False,
                showmeans=True,
                meanline=True,
                medianprops=propriedades_medianas,
                meanprops=propriedades_medias,
                flierprops={"marker": "+"},
                patch_artist=True,
            )
            # Coloca label vermelho na familia referencia

            if labelcores:
                for label, familia in zip(ax1.get_yticklabels(), self.familias):
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
            # Define o offset do dos textos
           
            if len(self.medias) < 3:
                offset = 1.1
            elif len(self.medias) < 4:
                offset = 1.2
            else:
                offset = 1.3
            for i in range(len(self.medias)):
            # Coloca valor do coeficiente de variação no boxplot
  
                if (cv):
                    x=(self.maximo[i])
                    # if self.CV[i]<15 and not self.maximo[i]==max(self.maximo):
                    #     x=self.maximo[i]+abs(self.medias[i])
                    # elif(abs(self.medias[i])<3) and not self.maximo[i]==max(self.maximo):
                    #     # print(i,"maximo",self.CV[i])
                    #     x=self.maximo[i]+abs(self.medias[i])
                    # else:
                    #     # print(i,"minimo",self.CV[i])
                    #     x=self.maximo[i]
                    ax1.text(x,i + offset-0.40,
                        "CV:{:.2f}%".format(self.CV[i]),
                        size=tamanho_texto,
                        color="black",
                        horizontalalignment="left", alpha=0.5
                            )
                # Coloca um texto com o valor da média de cada coluna no grafico
                if (valor_media):
                        if abs(self.medias[i]) > 1000000:
                            ax1.text(self.medias[i],i + offset,
                                "{:.0f}".format(self.medias[i]),
                                size=tamanho_texto,
                                color=verde,
                                horizontalalignment="center",
                            )
                            
                        elif abs(self.medias[i]) > 1000:
                            ax1.text(
                                self.medias[i],
                                i + offset,
                                "{:.1f}".format(self.medias[i]),
                                size=tamanho_texto,
                                color=verde,
                                horizontalalignment="center",
                            )
                            
                        elif abs(self.medias[i]) > 50:
                            ax1.text(
                                self.medias[i],
                                i + offset,
                                "{:.2f}".format(self.medias[i]),
                                size=tamanho_texto,
                                color=verde,
                                horizontalalignment="center",
                            )
                            
                        elif abs(self.medias[i]) > 1:
                            ax1.text(
                                self.medias[i],
                                i + offset,
                                "{:.3f}".format(self.medias[i]),
                                size=tamanho_texto,
                                color=verde,
                                horizontalalignment="center",
                            )
                        elif abs(self.medias[i]) > 0.1:
                            ax1.text(
                                self.medias[i],
                                i + offset,
                                "{:.4f}".format(self.medias[i]),
                                size=tamanho_texto,
                                color=verde,
                                horizontalalignment="center",
                            )
                        elif abs(self.medias[i]) > 0.001:
                            ax1.text(
                                self.medias[i],
                                i + offset,
                                "{:.6f}".format(self.medias[i]),
                                size=tamanho_texto,
                                color=verde,
                                horizontalalignment="center",
                            )    
                        else:
                            ax1.text(
                                self.medias[i],
                                i + offset,
                                "{}".format(self.medias[i]),
                                size=tamanho_texto,
                                color=verde,
                                horizontalalignment="center",
                            )
                        
            
            
            # Aplica configuração dos texto no grafico
            ax1.set_title(self.titulo, fontsize=tamanho_texto_super_grande, fontweight="bold")
            ax1.set_xlabel(self.eixox, fontsize=tamanho_texto_eixo, fontweight="bold")
            ax1.set_ylabel(self.eixoy, fontsize=tamanho_texto_eixo, fontweight="bold")
            for yticklabel in ax1.get_yticklabels():
                yticklabel.set_fontsize(tamanho_texto_eixo)
            for xticklabel in ax1.get_xticklabels():
                xticklabel.set_fontsize(tamanho_texto_eixo)
  
     
            fig1.tight_layout()
            # Faz a linha media do ensaio de referencia  se comMedia=True(ultimo)

            if linha_media:
                for i, familia in enumerate(self.familias):
                    if (
                        familia.lower() == "referencia"
                        or familia.lower() == "referência"
                        or familia.lower() == "ref"
                        or familia.lower() == "reference"
                        or familia.lower() == "ref."
                    ):
                        ax1.axvline(
                            self.medias[i],
                            ymin=0,
                            ymax=len(self.medias),
                            linewidth=1,
                            color=verde,
                            linestyle=":",
                        )

            # pinta cada boxplot com a cor de sua familia
            legenda = []
            incluido = []
            # cria legenda já com suas cores
            for patch, color in zip(graf["boxes"], self.familias):
                patch.set_facecolor(corGrafico[color])
                if color not in incluido:
                    incluido.append(color)
                    legenda.append(mpatches.Patch(color=corGrafico[color], label=color))
            legenda.reverse()
            # constroi a legenda
            if not(posicao_legenda=="NA"): # Se a posição foi diferente de NA
                ax1.legend(handles=legenda,framealpha =0.6,loc=int(posicao_legenda)).set_draggable(True)
            # mostra o grafico
            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            # print("retornando buffer")
            return buffer
        else:
            return False



# Função que cria o objeto e chama as funções 
def gera_boxplot(arquivo, linha_media,valor_media,cv, labelcores,legenda):
    boxplot=Boxplot(arquivo)
    print("Carregou boxplot")
    boxplot.le_dados() # faz a leitura dos dados do arquivo
    print("Leu dados\n",boxplot.dados)
    print(f"Status={boxplot.status()}")
    if boxplot.status(): # Se não ocorrer nenum erro
        boxplot.limpa_dados() # limpa os dados incoerentes e celulas vazias
    if (linha_media or valor_media) and boxplot.status: # Se não ocorrer nenum erro e for necessário exibir as médias
        boxplot.calcula_medias() # calcula as medias
    if boxplot.status(): # Se não ocorrer nenum erro
        boxplot.organiza_dados() # organiza os dados
    if boxplot.status(): # Se não ocorrer nenum erro
        grafico=boxplot.gera_grafico(linha_media,valor_media,cv,labelcores,legenda) # gera o gráfico
    else: #caso contraria retorne False
        grafico=boxplot.erro # Reporta os erros cometidos
    return grafico

