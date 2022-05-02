from django.urls import path
from .views import *
from .import views

app_name = 'cnfiguracoes'

urlpatterns = [
    # PAGINA principal
    path('arquivos/', views.pageUploadArquivos, name="upload-arquivos"),

    path('upload-saldo/', views.uploadSaldo, name="upload-saldo"),
    path('upload-vencimentorf/', views.uploadVencimentoRF, name="upload-vencimentorf"),
    path('upload-destaquerf/', views.uploadDestaqueRF, name="upload-destaquerf"),
    path('upload-custodiafii/', views.uploadCustodiaFII, name="upload-custodiafii"),
    path('upload-custodiarv/', views.uploadCustodiaRV, name="upload-custodiarv"),
]
