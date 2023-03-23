from django.urls import path
from . import views

urlpatterns = [path("",views.home, name="home"),
               path('menuEquipoamento/',views.menuEquipoamento,name="menuEquipoamento"),
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
               path('cadastrarTipo/',views.cadastrarTipo,name="cadastrarTipo"),
               path('listarTipo/',views.listarTipo,name="listarTipo"),
               path('editarTipo/',views.editarTipo,name="editarTipo"),
               path('baixarRelatorioEquipamentos/',views.baixarRelatorioEquipamentos,name="baixarRelatorioEquipamentos"),
               path('cadastrarMaterial/',views.cadastrarMaterial,name="cadastrarMaterial"),
               path('editarMaterial/',views.editarMaterial,name="editarMaterial"),
               path('listarMaterial/',views.listarMaterial,name="listarMaterial"),
               path('cadastrarArquivo/',views.cadastrarArquivo,name="cadastrarArquivo"),
               path('download_arquivo/',views.download_arquivo,name="download_arquivo"),
               path('excluirEquipamento/',views.excluirEquipamento,name="excluirEquipamento"),
               path('excluiArquivo/',views.excluiArquivo,name="excluiArquivo"),
               path('excluirTipo/',views.excluirTipo,name="excluirTipo"),
               path('excluirLocal/',views.excluirLocal,name="excluirLocal"),
]


