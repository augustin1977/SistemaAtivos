from django.urls import path
from . import views
import boxplot

urlpatterns = [
    path('ferramentas',boxplot.views.ferramentas,name='ferramentas'),
    path('criarboxplot2',boxplot.views.boxplotinicial2,name='boxplotinicial2'),
    path('gerar_grafico2/',boxplot.views.gerar_grafico2,name='gerar_grafico2'),
    path('download_model_csv2/', boxplot.views.download_model_csv2, name='download_model_csv2'),
    path('converte_intemperismo/',boxplot.views.converte_intemperismo,name='converte_intemperismo'),
    path('gerar_arquivo_intemperismo/',boxplot.views.gerar_arquivo_intemperismo,name='gerar_arquivo_intemperismo'),
    path('converte_OCR/',boxplot.views.converte_OCR,name='converte_OCR'),
    path('gerar_arquivo_OCR/',boxplot.views.gerar_arquivo_OCR,name='gerar_arquivo_OCR'),
    path('gerar_arquivo_moinho_piloto/',boxplot.views.gerar_arquivo_moinho_piloto,name='gerar_arquivo_moinho_piloto'),
    path('converte_moinho_piloto/',boxplot.views.converte_moinho_piloto,name='converte_moinho_piloto'),
    path('criarboxplot3',boxplot.views.boxplotinicial3,name='boxplotinicial3'),
    path('gerar_grafico3/',boxplot.views.gerar_grafico3,name='gerar_grafico3'),
    path('download_model_csv3/', boxplot.views.download_model_csv3, name='download_model_csv3'),
    path('calcula_energia_ruptura/', boxplot.views.calcula_energia_ruptura, name='calcula_energia_ruptura'),
    path('fact/', views.upload_fact, name='upload_fact'),
    path('fact/download/', views.download_excel_fact, name='download_excel_fact'),
    ]

