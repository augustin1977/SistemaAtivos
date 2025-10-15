from django.urls import path
from . import views

urlpatterns = [path("cores/cadastrar/",views.cadastra_cores, name="cadastra_cores"),
               path("cores/",views.exibe_cores, name="exibe_cores"),
               path("cores/editar/<int:id>/",views.edita_cores, name="edita_cores"),
               path("cores/deletar/<int:id>/",views.deleta_cores, name ="deleta_cores"),
               path("projetos/cadastrar/",views.cadastra_projetos, name="cadastra_projetos"),
               path("projetos/",views.exibe_projetos, name="exibe_projetos"),
               path("projetos/editar/<int:id>/",views.edita_projetos, name="edita_projetos"),
               path("projetos/deletar/<int:id>/",views.deleta_projetos, name="deleta_projetos"),
               path("projetos/desativar/<int:id>/", views.desativa_projetos, name="desativa_projetos"),
               path("projetos/ativar/<int:id>/", views.ativa_projetos, name="ativa_projetos"),
               path("projetos/inativos/", views.exibe_projetos_inativos, name="exibe_projetos_inativos"),
               path("amostras/cadastrar/",views.cadastra_amostras, name="cadastra_amostras"),
               path("amostras/",views.exibe_amostras, name="exibe_amostras"),
               path("amostras/editar/<int:id>/",views.edita_amostras, name="edita_amostras"),
               path("amostras/deletar/<int:id>/",views.deleta_amostras, name="deleta_amostras"),
               path("etiquetas/cadastrar/",views.cadastra_etiquetas, name="cadastra_etiquetas"),
               path("etiquetas/",views.exibe_etiquetas, name="exibe_etiquetas"),
               path("etiquetas/editar/<int:id>/",views.edita_etiquetas, name="edita_etiquetas"),
               path("etiquetas/deletar/<int:id>/",views.deleta_etiquetas, name="deleta_etiquetas"),
               path("etiquetas/imprimir/<int:id>",views.imprime_etiquetas, name="imprime_etiquetas"),
               ]