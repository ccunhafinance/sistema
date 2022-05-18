from django.urls import path
from .views import *
from .import views

app_name = 'tarefas'

urlpatterns = [
    # PAGINA principal
    path('', views.mainPageTarefas, name="tarefas-main"),
    path('registrorf/', views.regitroVencimentoRF, name="registra-tarefa"),
    path('clientes-positivos/', views.clientesPositivos, name="clientes-positivos"),
    path('clientes-negativos/', views.clientesNegativos, name="clientes-negativos"),
    # Novo
    path('vencimentosrf/', views.getVencimentoRFtoJson, name="vencimentosrf"),

]
