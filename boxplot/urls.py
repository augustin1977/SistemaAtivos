from django.urls import path
from . import views
import boxplot

urlpatterns = [
    path('ferramentas',boxplot.views.ferramentas,name='ferramentas'),
    path('criarboxplot',boxplot.views.boxplotinicial2,name='boxplotinicial'),
    path('gerar_grafico/',boxplot.views.gerar_grafico2,name='gerar_grafico'),
    path('download_model_csv/', boxplot.views.download_model_csv, name='download_model_csv'),
    path('converte_intemperismo/',boxplot.views.converte_intemperismo,name='converte_intemperismo'),
    path('gerar_arquivo_intemperismo/',boxplot.views.gerar_arquivo_intemperismo,name='gerar_arquivo_intemperismo'),
    path('converte_OCR/',boxplot.views.converte_OCR,name='converte_OCR'),
    path('gerar_arquivo_OCR/',boxplot.views.gerar_arquivo_OCR,name='gerar_arquivo_OCR'),

    ]
