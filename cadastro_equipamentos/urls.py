"""cadastro_equipamentos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from equipamentos import views
import boxplot.views
#from boxplot import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('notas/', include('notas.urls')),
    path('equipamentos/', include('equipamentos.urls')),
    path('auth/', include('usuarios.urls')),
    path('', include('usuarios.urls')),
    path('log/', include('log.urls')),
    path('consulta_dados_sistema/', views.consulta_dados_sistema, name='consulta_dados_sistema'),
    path('estatisticas/', views.consulta_dados_sistema, name='estatisticas'),
    path('estatistica/', views.consulta_dados_sistema, name='estatistica'),
    path('criarboxplot',boxplot.views.boxplotinicial2,name='boxplotinicial'),
    path('gerar_grafico/',boxplot.views.gerar_grafico2,name='gerar_grafico'),
    path('download_model_csv/', boxplot.views.download_model_csv, name='download_model_csv'),

]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
        

