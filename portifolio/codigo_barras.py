from django.utils.text import slugify
from .models import Etiqueta
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
import re
import unicodedata
from datetime import datetime


def gerar_codigo_limpo(nome_projeto: str) -> str:


    # 🔤 Normaliza acentuação e deixa em maiúsculo
    nome_limpo = unicodedata.normalize('NFKD', nome_projeto).encode('ASCII', 'ignore').decode('utf-8').upper()
    nome_limpo = re.sub(r'[^A-Z0-9 ]+', '', nome_limpo).strip()

    # 🔢 Detecta número no final (ex: "PROJETO 2")
    match = re.search(r'(\d+)$', nome_limpo)
    numero_final = match.group(1) if match else ''
    nome_base = nome_limpo[:match.start()] if match else nome_limpo
    palavras = nome_base.split()

    # 🧩 Divide caracteres entre as palavras
    total_letras = 8 - len(numero_final)
    partes = []

    if len(palavras) == 1:
        partes.append(palavras[0][:total_letras])
    else:
        # Divide de forma justa entre as palavras
        quota = total_letras // len(palavras)
        resto = total_letras % len(palavras)
        for i, p in enumerate(palavras):
            extra = 1 if i < resto else 0
            partes.append(p[:quota + extra])

    codigo = ''.join(partes) + numero_final
    return codigo[:8].upper()

def gerar_codigo_humano(amostra):
    """Gera um código humano único baseado no projeto e amostra."""
    projeto = amostra.projeto
    prefixo_projeto = gerar_codigo_limpo(projeto.nome)
    prefixo_amostra = gerar_codigo_limpo(amostra.nome)

    # Buscar o último código desse projeto/amostra
    existentes = Etiqueta.objects.filter(amostra__projeto=amostra.projeto).count()
    seq = str(existentes + 1).zfill(4)

    # Garantir unicidade (repetir até achar um livre)
    while True:
        codigo = f"{prefixo_projeto}-{prefixo_amostra}-{seq}"
        if not Etiqueta.objects.filter(codigo_humano=codigo).exists():
            return codigo
        existentes += 1
        seq = str(existentes + 1).zfill(4)

def gerar_codigo_numerico():
    """Gera um código numérico sequencial global."""
    ultimo = Etiqueta.objects.order_by('-id').first()
    proximo = (ultimo.id + 1) if ultimo else 1
    return f"{proximo:09d}"


def gerar_codigo_barras(codigo_numerico):
    """Gera o código de barras (Code128) e retorna em bytes (PNG)."""
    buffer = BytesIO()
    barcode_class = barcode.get_barcode_class('code128')
    barcode_obj = barcode_class(codigo_numerico, writer=ImageWriter())
    barcode_obj.write(buffer)
    buffer.seek(0)
    return ContentFile(buffer.read(), name=f"{codigo_numerico}.png")



def gerar_pdf_etiquetas(etiquetas, usuario=None):
    """
    Gera PDF A4 com 12 etiquetas (2 colunas x 6 linhas),
    borda colorida, layout horizontal e informações completas.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    # 🔧 Configurações do layout
    etiquetas_por_linha = 2
    linhas_por_pagina = 6
    margem_esq = 8 * mm
    margem_sup = 10 * mm
    espacamento_h = 6 * mm
    espacamento_v = 4 * mm
    
    

    largura_etiqueta = (largura - margem_esq * 2 - espacamento_h) / etiquetas_por_linha
    altura_etiqueta = (altura - margem_sup * 2 - (linhas_por_pagina - 1) * espacamento_v) / linhas_por_pagina

    x_inicial = margem_esq
    y_inicial = altura - margem_sup -  altura_etiqueta 
    x = x_inicial
    y = y_inicial
    total_por_pagina = etiquetas_por_linha * linhas_por_pagina
    
    empresa = "Instituto de Pesquisas Tecnológicas - IPT"
    laboratorio = "Laboratório de Processos Metalurgicos - LPM"

    for contador, etiqueta in enumerate(etiquetas):
        indice_pagina = contador % total_por_pagina
        linha = indice_pagina // etiquetas_por_linha
        coluna = indice_pagina % etiquetas_por_linha

        # Coordenadas da etiqueta
        x = margem_esq + coluna * (largura_etiqueta + espacamento_h)
        y = altura - margem_sup - (linha + 1) * altura_etiqueta - linha * espacamento_v

        # Coordenadas da etiqueta
        x = margem_esq + coluna * (largura_etiqueta + espacamento_h)
        y = altura - margem_sup - (linha + 1) * altura_etiqueta - linha * espacamento_v

        cor = getattr(etiqueta.amostra.projeto.cor, "css_color", "#cccccc")

        # Fundo branco com borda colorida
        c.setStrokeColor(cor)
        c.setLineWidth(2)
        c.setFillColor(colors.white)
        c.rect(x, y, largura_etiqueta, altura_etiqueta, fill=True, stroke=True)

        # Cabeçalho - Empresa e Laboratório
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.black)
        c.drawString(x + 5 * mm, y + altura_etiqueta - 7 * mm, empresa)
        c.drawString(x + 5 * mm, y + altura_etiqueta - 10 * mm, laboratorio)

        # Projeto e Amostra
        c.setFont("Helvetica", 8)
        c.drawString(x + 5 * mm, y + altura_etiqueta - 13 * mm, f"Projeto: {etiqueta.amostra.projeto.nome}")
        c.drawString(x + 5 * mm, y + altura_etiqueta - 15.5 * mm, f"Amostra: {etiqueta.amostra.nome}")
        c.drawString(x + 5 * mm, y + altura_etiqueta - 18 * mm, f"Responsável: {etiqueta.amostra.projeto.responsavel}")

        # Código humano
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 5 * mm, y + altura_etiqueta - 22 * mm, f"{etiqueta.codigo_humano}")

        # Código de barras
        barcode = code128.Code128(etiqueta.codigo_numerico, barHeight=15 * mm, barWidth=0.9)
        barcode_x = x + 51 * mm
        barcode_y = y + 15 * mm
        barcode.drawOn(c, barcode_x, barcode_y )

        # Código numérico impresso abaixo do código de barras
        c.setFont("Helvetica", 8)
        c.drawCentredString(barcode_x +20*mm, barcode_y-3*mm, etiqueta.codigo_numerico)

        # Massa e Local de Instalação
        c.setFont("Helvetica", 7)
        c.drawString(x + 5 * mm, y + 13 * mm, f"Massa (kg): {etiqueta.massa or '___________________________'}")
        c.drawString(x + 5 * mm, y + 5 * mm, f"observação: {etiqueta.observacao or '___________________________'} ")
        c.drawString(x + 5 * mm, y + 1 * mm, f"{etiqueta.local_instalacao}")
        
        # identifcação do usuario e data/hora de geração
        c.setFont("Helvetica", 4.5)
        c.saveState()
        data_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        texto_user = f"Gerado por: {usuario}" if usuario else "Gerado automaticamente"
        c.translate(x + largura_etiqueta - 6 * mm, y)
        c.rotate(90)
        c.drawString(0.25 * mm, -5 * mm, f"{texto_user} – {data_str}")
        c.restoreState()  # Restaura o estado (impede rotações acumuladas)
        # Faixa superior colorida (opcional)
        c.setFillColor(cor)
        c.rect(x, y + altura_etiqueta - 3 * mm, largura_etiqueta, 3 * mm, fill=True, stroke=False)

        #  Nova página a cada 12 etiquetas
        if (contador + 1) % total_por_pagina == 0:
            c.showPage()  # 👉 muda de página
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.black)

    c.save()
    buffer.seek(0)
    return buffer
