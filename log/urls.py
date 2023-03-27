from django.urls import path
from . import views

urlpatterns = [path("relatorioLog/",views.relatorioLog, name="relatorioLog"),
                path("baixarRelatorioLog/",views.baixarRelatorioLog, name="baixarRelatorioLog"),   
               

]
