from django.urls import path
from .views import *
from .import views

app_name = 'tarefas'

urlpatterns = [
    # PAGINA principal
    path('aniversarios', views.aniversarios, name="aniversarios"),
    path('vencimentorf', views.vencimentorf, name="vencimentorf"),
    path('saldopositivo', views.saldopositivo, name="saldopositivo"),
    path('saldonegativo', views.saldonegativo, name="saldonegativo"),



    path('registrorf/', views.regitroVencimentoRF, name="registra-tarefa"),
    path('clientes-positivos/', views.clientesPositivos, name="clientes-positivos"),
    path('clientes-negativos/', views.clientesNegativos, name="clientes-negativos"),
    # Novo
    path('vencimentosrf/', views.getVencimentoRFtoJson, name="vencimentosrf"),

]
