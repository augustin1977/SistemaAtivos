from django.urls import path
from . import views



urlpatterns = [path('notas/',views.notas,name="notas"),
               path('cadastrarDisciplina/',views.cadastrarDisciplina,name="cadastrarDisciplina"),
               path('cadastrarModo_Falha/',views.cadastrarModo_Falha,name="cadastrarModo_Falha"),
               path('cadastrarModo_FalhaEquipamento/',views.cadastrarModo_FalhaEquipamento,name="cadastrarModo_FalhaEquipamento"),
               path('cadastrarNota/',views.cadastrarNota,name="cadastrarNota"),
               path('get_modos_de_falha/', views.get_modos_de_falha, name='get_modos_de_falha'),
               path('exibirDisciplinas/', views.exibirDisciplinas, name='exibirDisciplinas'),
               path('editarDisciplina/', views.editarDisciplina, name='editarDisciplina'),
               path('excluirDisciplina/', views.excluirDisciplina, name='excluirDisciplina'),
               path('exibirModoFalha/', views.exibirModoFalha, name='exibirModoFalha'),
               path('editarModoFalha/', views.editarModoFalha, name='editarModoFalha'),
               path('excluirModoFalha/', views.excluirModoFalha, name='excluirModoFalha'),
               path('exibirModoFalhaEquipamento/', views.exibirModoFalhaEquipamento, name='exibirModoFalhaEquipamento'),
               path('editarModoFalhaEquipamento/', views.editarModoFalhaEquipamento, name='editarModoFalhaEquipamento'),
               path('excluirModoFalhaEquipamento/', views.excluirModoFalhaEquipamento, name='excluirModoFalhaEquipamento'),
               path('exibirNotas/', views.exibirNotas, name='exibirNotas'),
               path('editarNotas/', views.editarNotas, name='editarNotas'),
               path('excluirNotas/', views.excluirNotas, name='excluirNotas'),
    
]
