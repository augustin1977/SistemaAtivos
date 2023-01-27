from django.urls import path
from . import views

urlpatterns = [path("",views.home, name="home"),
               path('listarEquipamentos/',views.lista_equipamentos, name='listar_equipamentos'),
               path('exibirDetalheEquipamento/',views.exibirDetalheEquipamento, name='exibirDetalheEquipamento'),
               path('download_view/',views.download_view,name="download"),
               path('cadastrarFornecedor/',views.cadastrarFornecedor,name="cadastrarFornecedor"),
               path('listarFornecedores/',views.listarFornecedores,name="listarFornecedores"),
               path('editarFornecedor/',views.editarFornecedor,name="editarFornecedor"),
               path('exibirDetalheFornecedor/',views.exibirDetalheFornecedor,name="exibirDetalheFornecedor"),
               path('cadastrarLocal/',views.cadastrarLocal,name="cadastrarLocal"),
               path('listarLocais/',views.listarLocais,name="listarLocais"),
               path('cadastrarEquipamento/',views.cadastrarEquipamento,name="cadastrarEquipamento"),
               path('editarEquipamento/',views.editarEquipamento,name="editarEquipamento"),
]


