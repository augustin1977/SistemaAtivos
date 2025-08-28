from django.shortcuts import render
from django.http import *
import boxplot.Converte_OCR
import boxplot.boxplot2 
import boxplot.boxplot3
import boxplot.integral_trapezios
import boxplot.csv_intemperismo_converter, boxplot.moinho_piloto_converter
from django.http import FileResponse
from django.shortcuts import render
import json
from boxplot.tabela_periodica import elementos as ELEMENTOS_TABELA
from boxplot.fact_utils import extrair_dados_generico, get_options, gerar_excel
import base64
import json


# Funçõres de geração de tela para entrada de dados

def ferramentas(request):
    return render(request, "ferramentas.html")

def converte_intemperismo(request):
    return render(request, "converte_imtemperismo.html")

def converte_OCR(request):
    return render(request,"OCR.html")
# funções de geração do BOXPLOT
def boxplotinicial2(request):
    return render(request, "boxplot2.html")
def gerar_grafico2(request):
    file = request.FILES.get("arquivoAnexo")
    name = str(file)
    if name[-3:] != "csv":
        # print(name[-3:])
        return render(request, "boxplot2.html", {"erro": "2"})
    escala_fixa=(request.POST.get("escala_fixa")=="on")
    minimo=0
    maximo=10
    if escala_fixa:
        try:
            minimo=float(request.POST.get("escala_minima"))
            maximo=float(request.POST.get("escala_maxima"))
        except:
            escala_fixa=False
            return render(request, "boxplot2.html", {"erro": "4"})
                        
    imagem = boxplot.boxplot2.gera_boxplot(
        file,
        request.POST.get("linha_media") == "on",
        request.POST.get("valor_media") == "on",
        request.POST.get("CV")=="on",
        request.POST.get("labelcores") == "on",
        request.POST.get("legenda"),
        escala_fixa,
        minimo,
        maximo
    )

    if imagem:
        response = HttpResponse(imagem, content_type="image/png")
        response["Content-Disposition"] = f"attachment; filename=boxplot.png"

        return response
    elif imagem == 3:  # Erro de decodificação
        return render(request, "boxplot2.html", {"erro": "3"})
    else:
        return render(request, "boxplot2.html", {"erro": "1"})
def download_model_csv2(request) -> FileResponse:
    """Return a file in csv in a model format to the user to generetar boxplot

    Args:
        request (None): None is requested

    Returns:
        _type_: file CSV with model to create a boxplot picture
    """
    # Crie o conteúdo do modelo CSV
    content = "Titulo;Legenda Eixo X;Legenda Eixo Y;;\nReferencia;Familia1;Familia1;Familia2;Familia2\nA;B;C;D;E\n1;4;1;5;9\n3;5;2;6;8\n3;3;3;7;7\n4;4;8;4;6\n5;6;5;6;7\n3;4;5;7;8\n4;5;8;8;8\n3;8;8;8;9\n2;7;4;9;9"

    # Crie uma resposta de arquivo para o modelo CSV
    response = HttpResponse(content, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="modelo.csv"'

    return response
# Funções de processamento dos arquivo de intemperismo
def gerar_arquivo_intemperismo(request):
    file = request.FILES.get("arquivoAnexo")
    name = str(file)
    opcao=request.POST.get("opcao")
    # print(opcao)
    nome=name[:-4]
    if name[-3:] != "csv":
        # print(name[-3:])
        return render(request, "converte_imtemperismo.html", {"erro": "2"})
    try:
        arquivo = boxplot.csv_intemperismo_converter.geraXLS(file,opcao)
    except Exception as mensagem:
        return render(request, "converte_imtemperismo.html", {"erro": "3", "mensagem":mensagem}) 
    if arquivo:
        response = HttpResponse(arquivo, content_type="application")
        response["Content-Disposition"] = f"attachment; filename={nome}.xlsx"

        return response
    elif arquivo == 3:  # Erro de decodificação
        return render(request, "converte_imtemperismo.html", {"erro": "3"})
    else:
        return render(request, "converte_imtemperismo.html", {"erro": "1"})

# funções de conversão do arquivo do moinho piloto
def converte_moinho_piloto(request):
    return render(request,"moinho_piloto.html")
def gerar_arquivo_moinho_piloto(request):
    file = request.FILES.get("arquivoAnexo")
    name = str(file)
    if name[-3:] != "log":
        # print(name[-3:])
        return render(request, "moinho_piloto.html", {"erro": "2"})
    # arquivo = boxplot.moinho_piloto_converter.geraXLS(file) # Só usado para diagnostico
    try:
        arquivo = boxplot.moinho_piloto_converter.geraXLS(file)
    except Exception as e:
        #print(e)
        return render(request, "moinho_piloto.html", {"erro": "3"}) 
    
    if arquivo:
        response = HttpResponse(arquivo, content_type="application")
        response["Content-Disposition"] = f"attachment; filename=resultado.xlsx"

        return response
    elif arquivo == 3:  # Erro de decodificação
        return render(request, "converte_moinho_piloto.html", {"erro": "3"})
    else:
        return render(request, "converte_moinho_piloto.html", {"erro": "1"})
    
# funções do conversor do OCR
def gerar_arquivo_OCR(request):
    file = request.FILES.get("arquivoAnexo")
    name = str(file)
    if name[-3:].upper() != "TXT":
        # print(name[-3:])
        return render(request, "OCR.html", {"erro": "2"})
    
    opcoes={'valor_maximo':request.POST.get('valorMaximo'), 
                'valor_minimo':request.POST.get('valorMinimo'), 
                'gradiente_maximo':request.POST.get('gradienteMaximo'), 
                'periodo_media':request.POST.get('periodoMedia'), 
                'confianca_minima':request.POST.get('confiancaMinima'),
                'grandeza':request.POST.get("nomeGrandeza")}
    
   
    arquivo = boxplot.Converte_OCR.geraXLS(file,opcoes)
    # except Exception as e:
    #     print(e)
        # return render(request, "OCR.html", {"erro": "3"}) 
    if arquivo:
        response = HttpResponse(arquivo, content_type="application")
        response["Content-Disposition"] = f"attachment; filename=resultado.xlsx"

        return response
    elif arquivo == 3:  # Erro de decodificação
        return render(request, "OCR.html", {"erro": "3"})
    else:
        return render(request, "OCR.html", {"erro": "1"})

def boxplotinicial3(request):
    return render(request, "boxplot3.html")

def gerar_grafico3(request):
    file = request.FILES.get("arquivoAnexo")
    name = str(file)
    # print(name)
    if name[-3:] != "csv":
        # print(name,"erro")
        return render(request, "boxplot3.html", {"erro": "2"})
    imagem,mensagemErro = boxplot.boxplot3.gera_boxplot(
        file,
        request.POST.get("linha_media") == "on",
        request.POST.get("valor_media") == "on",
        request.POST.get("CV")=="on",
        request.POST.get("labelcores") == "on",
        request.POST.get("legenda"),
        int(request.POST.get("graficolegenda"))
    )
    # print(f"view imagem={imagem}")
    if imagem == 3:  # Erro de decodificação
        return render(request, "boxplot3.html", {"erro": "3","mensagemErro":mensagemErro})
    elif imagem:
        response = HttpResponse(imagem, content_type="image/png")
        response["Content-Disposition"] = f"attachment; filename=boxplot.png"

        return response
    if imagem == 3:  # Erro de decodificação
        return render(request, "boxplot3.html", {"erro": "3","mensagemErro":mensagemErro})
    else:
        return render(request, "boxplot3.html", {"erro": "1"})

def download_model_csv3(request) -> FileResponse:
    """Retorna um arquivoi CSV modelo para gerar o boxplot

    Argumentos:
        nenhum argumento é necessário, request=None

    Retorna:
        Retorna um arquivo CSV para gerar o boxplot
    """
    # Crie o conteúdo do modelo CSV
    content = """Titulo;Legenda Eixo X;Legenda Eixo Y;;;;;;;;;;;;;;
G1;G2;G3;G1;G1;G1;G1;G1;G1;G2;G2;G2;G3;G3;G3;G3;G3
Referencia;Referencia;Referencia;Familia1;Familia1;Familia2;Familia3;Familia2;Familia2;Familia4;Familia2;Familia1;Familia5;Familia1;Familia3;Familia4;Familia4
Referencia;Referencia;Referencia;A;B;C;D;E;F;A;B;C;A;C;D;F;G
1;2;1;5;4;1;5;5;5;8;8;5;9;1;1;2;15
2;3;3;6;4;2;6;6;5;8;9;6;8;2;2;6;16
3;4;5;7;5;3;7;7;3;9;8;7;7;3;3;7;17
4;5;7;8;5;1;5;5;4;9;9;8;8;4;4;8;15
5;6;9;9;6;2;5;5;5;8;8;9;5;5;5;5;12
1;2;11;10;6;3;4;3;5;8;9;10;7;6;6;3;18
2;3;13;7;6;4;6;6;7;8;8;7;8;7;7;6;22
3;4;15;8;4;7;5;4;8;8;7;8;10;8;8;4;1
11;5;17;6;7;3;6;6;6;9;7;6;12;9;9;5;5
12;6;10;7;1;5;7;7;7;9;8;7;9;5;5;7;17
"""
    # Crie uma resposta de arquivo para o modelo CSV
    response = HttpResponse(content, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="modelo.csv"'

    return response

def calcula_energia_ruptura(request):
    if request.method=="GET":
        return render(request, "calcula_energia_ruptura.html",{"lista":[]})
    else:
        #print(request.POST.get("opcao"))
        arquivo=request.FILES.get("arquivoAnexo")   
        if arquivo:  
            if request.POST.get("opcao")=="Maquina1":
                dados=boxplot.integral_trapezios.decodifica_Shimatsu(arquivo)
            elif request.POST.get("opcao")=="Maquina2":
                dados=boxplot.integral_trapezios.decodifica_EMIC(arquivo)
            elif request.POST.get("opcao")=="Maquina3":
                dados=boxplot.integral_trapezios.decodifica_MEC_ROCHAS(arquivo)
            else:
                return render(request, "calcula_energia_ruptura.html",{"lista":[],"erro":"3"})
            energia=boxplot.integral_trapezios.calcula_energia(dados)
            request.session["dados_armazenados"] = json.dumps(dados)
            return render(request, "calcula_energia_ruptura.html",{"lista":energia})
        
        dados=json.loads(request.session["dados_armazenados"])
        selecionados = request.POST.getlist("selecionados")
        grafico_url = boxplot.integral_trapezios.gerar_grafico_forca_deslocamento(dados, selecionados)
        if grafico_url:
            
            response = HttpResponse(grafico_url, content_type="image/png")
            response["Content-Disposition"] = f"attachment; filename=Forca_deslocamento.png"

            return response
        energia=boxplot.integral_trapezios.calcula_energia(dados)
        return render(request, "calcula_energia_ruptura.html",{"lista":energia,"erro":"1"})

def upload_fact(request):
    if request.method == "POST":
        arquivo = request.FILES.get("arquivo")
        if not arquivo:
            return render(request, "upload_fact.html", {"erro": "Nenhum arquivo enviado."})

        try:
            text = arquivo.read().decode("utf-8")
        except Exception as e:
            return render(request, "upload_fact.html", {"erro": f"Erro ao ler o arquivo: {e}"})

        records = extrair_dados_generico(text)
        options, elementos_presentes = get_options(records)

        records_json = json.dumps(records)
        records_b64 = base64.b64encode(records_json.encode("utf-8")).decode("utf-8")

        return render(request, "seleciona_elementos.html", {
            "elementos": ELEMENTOS_TABELA,
            "elementos_presentes": elementos_presentes,
            "fases": list(options.keys()),
            "records_b64": records_b64
        })

    return render(request, "upload_fact.html")


def download_excel_fact(request):
    if request.method == "POST":
        records_b64 = request.POST.get("records_b64")
        elementos_selecionados = request.POST.getlist("elementos")
        fases_selecionadas = request.POST.getlist("fases")

        try:
            records = json.loads(base64.b64decode(records_b64).decode("utf-8"))
        except Exception as e:
            return HttpResponse(f"Erro ao decodificar os dados: {e}")

        return gerar_excel(records, elementos_selecionados, fases_selecionadas)

    return HttpResponse("Requisição inválida.")


