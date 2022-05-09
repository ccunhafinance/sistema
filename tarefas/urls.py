from django.urls import path
from .views import *
from .import views

app_name = 'tarefas'

urlpatterns = [
    # PAGINA principal
    path('', views.mainPageTarefas, name="tarefas-main"),
    path('registrorf/', views.regitroVencimentoRF, name="registra-tarefa"),
]
