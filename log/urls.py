from django.urls import path
from . import views

urlpatterns = [path("menuRelatorios/",views.menuRelatorios, name="menuRelatorios"),
    path("relatorioLog/",views.relatorioLog, name="relatorioLog"),
    path("baixarRelatorioLog/",views.baixarRelatorioLog, name="baixarRelatorioLog"), 
    path("baixarRelatorioEquipamento/",views.baixarRelatorioEquipamento, name="baixarRelatorioEquipamento"), 
    path("relatorioNotasEquipamento/",views.relatorioNotasEquipamento, name="relatorioNotasEquipamento"),   
]
