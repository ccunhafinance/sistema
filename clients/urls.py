from django.urls import path
from .views import *
from .import views

app_name = 'clients'

urlpatterns = [
  # PAGINA MEUS CLIENTES
  path('meus-clientes/', views.meusClientes, name="clients-list"),
  # PAGINA ONBOARDING
  path('onboarding/', views.onBording, name="clients-onboarding"),
  #  PAGINA ONBOARDING
  path('espelhamento/', views.espelhamento, name="mirror-list"),

  path('mirror/add/', views.mirroradd, name="mirror-add"),
  path('upload-cliente/', views.upload_clientes, name="upload_clientes"),
  path('rotina-emails/<int:id>', views.rotina_emails, name="rotina_emails"),
  path('delete-all/', views.delet_all, name="delet_all"),
  path('update_cliente_novo/', views.update_new_cliente, name="update_cliente_novo"),
  path('update_troca_assessor/', views.update_troca_assessor, name="update_troca_assessor"),
  path('update_troca_assessor_externo/', views.update_troca_assessor_externo, name="update_troca_assessor_externo"),
  path('url_google_sheets/', views.google_sheets, name="url_google_sheets"),
  path('mirror/delete/<int:pk>/', views.mirrordelete, name="mirror-delete"),
  path('mirror/get-cliente-data/', views.get_cliente_data, name="get-cliente-data"),
  path('questionario-inove-investimentos/<str:id>/<str:token>/', views.cliente_responde, name="cliente-responde"),
  path('obrigado/', views.obrigado_questionario, name="obrigado-questionario"),
  path('teste_insert/', views.teste_insert, name="obrigado-questionario"),
  path('get-my-clients/', views.getMyClients, name="get-my-clientes"),
  path('update_observacao/', views.update_observacao, name="update-observacao"),
  path('send_email_ondemand/', views.send_email_ondemand, name="mail-ondemand"),
  path('update-onbord/', views.updateOnbording, name="update-onbord"),
]
