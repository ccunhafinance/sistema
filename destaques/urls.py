from django.urls import path
from .views import *
from .import views

app_name = 'destaques'

urlpatterns = [
    # PAGINA principal
    path('renda-fixa/', views.pageDestaqueRendaFixa, name="renda-fixa"),
    path('semana/', views.pageDestaqueSemana, name="semana"),
]
