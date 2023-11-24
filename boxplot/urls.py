from django.urls import path
from . import views
import boxplot

urlpatterns = [
    path('criarboxplot',boxplot.views.boxplotinicial2,name='boxplotinicial'),
    path('gerar_grafico/',boxplot.views.gerar_grafico2,name='gerar_grafico'),
    path('download_model_csv/', boxplot.views.download_model_csv, name='download_model_csv'),
    ]