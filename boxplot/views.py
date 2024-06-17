from django.shortcuts import render
from django.http import *
import boxplot.Converte_OCR
import boxplot.boxplot2 
import boxplot.csv_intemperismo_converter, boxplot.moinho_piloto_converter
from django.http import FileResponse
from django.shortcuts import render

# Funçõres de geração de tela para entrada de dados
def boxplotinicial2(request):
    return render(request, "boxplot.html")
def ferramentas(request):
    return render(request, "ferramentas.html")

def converte_intemperismo(request):
    return render(request, "converte_imtemperismo.html")

def converte_OCR(request):
    return render(request,"OCR.html")
# funções de geração do BOXPLOT
def gerar_grafico2(request):
    file = request.FILES.get("arquivoAnexo")
    name = str(file)
    if name[-3:] != "csv":
        # print(name[-3:])
        return render(request, "boxplot.html", {"erro": "2"})
    imagem = boxplot.boxplot2.gera_boxplot(
        file,
        request.POST.get("linha_media") == "on",
        request.POST.get("valor_media") == "on",
        request.POST.get("CV")=="on",
        request.POST.get("labelcores") == "on",
        request.POST.get("legenda")  
    )

    if imagem:
        response = HttpResponse(imagem, content_type="image/png")
        response["Content-Disposition"] = f"attachment; filename=boxplot.png"

        return response
    elif imagem == 3:  # Erro de decodificação
        return render(request, "boxplot.html", {"erro": "3"})
    else:
        return render(request, "boxplot.html", {"erro": "1"})
def download_model_csv(request) -> FileResponse:
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
    
    if name[-3:] != "csv":
        # print(name[-3:])
        return render(request, "converte_imtemperismo.html", {"erro": "2"})
    try:
        arquivo = boxplot.csv_intemperismo_converter.geraXLS(file,opcao)
    except Exception as mensagem:
        return render(request, "converte_imtemperismo.html", {"erro": "3", "mensagem":mensagem}) 
    if arquivo:
        response = HttpResponse(arquivo, content_type="application")
        response["Content-Disposition"] = f"attachment; filename=resultado.xlsx"

        return response
    elif arquivo == 3:  # Erro de decodificação
        return render(request, "converte_imtemperismo.html", {"erro": "3"})
    else:
        return render(request, "converte_imtemperismo.html", {"erro": "1"})

# funções de conversão do arquivo do moinho piloto
def gerar_arquivo_moinho_piloto(request):
    file = request.FILES.get("arquivoAnexo")
    name = str(file)
    if name[-3:] != "log":
        # print(name[-3:])
        return render(request, "converte_moinho_piloto.html", {"erro": "2"})
    try:
        arquivo = boxplot.moinho_piloto_converter.geraXLS(file)
    except:
        return render(request, "converte_moinho_piloto.html", {"erro": "3"}) 
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
