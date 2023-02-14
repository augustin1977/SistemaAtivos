from django.urls import path
from . import views

urlpatterns = [path("listarLog/",views.listarLog, name="listarLog"),
                path("baixarRelatorioLog/",views.baixarRelatorioLog, name="baixarRelatorioLog"),   
               

]
