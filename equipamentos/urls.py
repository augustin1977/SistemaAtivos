from django.urls import path
from . import views

urlpatterns = [path("",views.home, name="home"),
               path('download_view/',views.download_view,name="download"),
               path('cadastrarFornecedor/',views.cadastrarFornecedor,name="cadastrarFornecedor"),
               path('listarFornecedores/',views.listarFornecedores,name="listarFornecedores"),
               path('editarFornecedor/',views.editarFornecedor,name="editarFornecedor"),
               path('exibirDetalheFornecedor/',views.exibirDetalheFornecedor,name="exibirDetalheFornecedor"),
               path('listarEquipamentos/',views.lista_equipamentos, name='listar_equipamentos'),
               path('cadastrarEquipamento/',views.cadastrarEquipamento,name="cadastrarEquipamento"),
               path('editarEquipamento/',views.editarEquipamento,name="editarEquipamento"),
               path('exibirDetalheEquipamento/',views.exibirDetalheEquipamento, name='exibirDetalheEquipamento'),
               path('cadastrarLocal/',views.cadastrarLocal,name="cadastrarLocal"),
               path('listarLocais/',views.listarLocais,name="listarLocais"),
               path('editarLocal/',views.editarLocal,name="editarLocal"),

]


