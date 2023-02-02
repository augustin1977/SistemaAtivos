from django.urls import path
from . import views
# cria os caminhos para acesso as views
from django.urls import path
from . import views
# cria os caminhos para acesso as views
urlpatterns = [
    path("cadastrar/",views.cadastrar, name="cadastrar"),
    path("editar/",views.editar, name="editar"),
    path("login/",views.login,name="login"),
    path("valida_cadastro/",views.valida_cadastro, name="valida_cadastro"),
    path("validar_login/",views.validar_login, name="validar_login"),
    path("sair/",views.sair, name="sair"),
    path("",views.login, name="vazio"),
]