from django.urls import path
from . import views



urlpatterns = [path('notas/',views.notas,name="notas"),
               path('cadastrarDisciplina/',views.cadastrarDisciplina,name="cadastrarDisciplina"),
               path('cadastrarModo_Falha/',views.cadastrarModo_Falha,name="cadastrarModo_Falha"),
               path('cadastrarModo_FalhaEquipamento/',views.cadastrarModo_FalhaEquipamento,name="cadastrarModo_FalhaEquipamento"),
               path('cadastrarNota/',views.cadastrarNota,name="cadastrarNota"),
               path('get_modos_de_falha/', views.get_modos_de_falha, name='get_modos_de_falha'),
    
]
