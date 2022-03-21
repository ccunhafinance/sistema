from django.urls import path
from .views import *
from .import views
app_name = 'clients'

urlpatterns = [
         path('', ListViewClients.as_view(), name="clients-list"),
         path('espelhamento/', ListMirrorView.as_view(), name="mirror-list"),
         path('mirror/add/', views.mirroradd, name="mirror-add"),
         path('upload-cliente/', views.upload_clientes, name="upload_clientes"),
         path('rotina-emails/<int:id>', views.rotina_emails, name="rotina_emails"),
         path('delete-all/', views.delet_all, name="delet_all"),
         path('update_cliente_novo/', views.update_new_cliente, name="update_cliente_novo"),
         path('update_troca_assessor/', views.update_troca_assessor, name="update_troca_assessor"),
         path('url_google_sheets/', views.google_sheets, name="url_google_sheets"),
         path('mirror/delete/<int:pk>/', views.mirrordelete, name="mirror-delete"),
         path('mirror/get-cliente-data/', views.get_cliente_data, name="get-cliente-data"),
         path('change-tipo-contato/', views.change_tipo_contato, name="change-tipo-contato"),
         path('change-frequencia-contato/', views.change_frequencia_contato, name="change-frequencia-contato"),
         path('acomp-perm/', views.acomp_perm, name="acomp-perm"),
         path('acomp-acomp_rf/', views.acomp_rf, name="acomp-rf"),
         path('acomp_acoes/', views.acomp_acoes, name="acomp-acoes"),
         path('acomp_fii/', views.acomp_fii, name="acomp-fii"),
         path('acomp_fiinvest/', views.acomp_fiinvest, name="acomp-fiinvest"),
         path('update_observacao/', views.update_observacao, name="update-observacao"),
         path('enviar_implement/', views.enviar_implement, name="enviar-implement"),
         path('enviar_sujest/', views.enviar_sujest, name="enviar-sugest"),
         path('perfil_preenchido/', views.perfil_preenchido, name="perfil-preenchido"),
         path('send_email_ondemand/', views.send_email_ondemand, name="mail-ondemand"),
         path('questionario/<str:id>/<str:token>/', views.cliente_responde, name="cliente-responde"),
         path('save_by_client/', views.save_by_client, name="save-by-client"),
         path('obrigado/', views.obrigado_questionario, name="obrigado-questionario"),

]
