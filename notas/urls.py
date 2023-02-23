from django.urls import path
from . import views



urlpatterns = [path('cadastrarDisciplina/',views.cadastrarDisciplina,name="cadastrarDisciplina"),
               path('cadastrarModo_Falha/',views.cadastrarModo_Falha,name="cadastrarModo_Falha"),
 
    
]
