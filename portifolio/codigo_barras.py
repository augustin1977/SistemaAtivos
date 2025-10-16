from django.utils.text import slugify
from .models import Etiqueta
import barcode
from barcode.writer import ImageWriter
from io import BytesIO

def gerar_codigo_humano(amostra):
    """Gera um código humano único baseado no projeto e amostra."""
    projeto = amostra.projeto
    prefixo_projeto = slugify(projeto.nome)[:4].upper()
    prefixo_amostra = slugify(amostra.nome)[:3].upper()

    ultimo = Etiqueta.objects.filter(amostra__projeto=projeto).order_by('-id').first()
    if ultimo and "-" in ultimo.codigo_humano:
        try:
            seq = int(ultimo.codigo_humano.split('-')[-1]) + 1
        except ValueError:
            seq = ultimo.id + 1
    else:
        seq = 1

    return f"{prefixo_projeto}-{prefixo_amostra}-{seq:05d}"


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
    barcode_obj.write(buffer, options={"module_height": 15.0, "font_size": 8})
    buffer.seek(0)
    return buffer.getvalue()