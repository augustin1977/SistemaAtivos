from django.urls import path
from . import views

urlpatterns = [path("",views.home, name="home"),
               path('listarEquipamentos/',views.lista_equipamentos, name='listar_equipamentos')
    
    
]
