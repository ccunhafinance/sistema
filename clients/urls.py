from django.urls import path
from .views import *
from .import views
app_name = 'appname'

urlpatterns = [
         path('', ListViewClients.as_view(), name="clients-list"),
         path('espelhamento/', ListMirrorView.as_view(), name="mirror-list"),
         path('mirror/add/', views.mirroradd, name="mirror-add"),
         path('upload-cliente/', views.upload_clientes, name="upload_clientes"),
         path('delete-all/', views.delet_all, name="delet_all"),
         path('mirror/delete/<int:pk>/', views.mirrordelete, name="mirror-delete"),
         path('mirror/get-cliente-data/', views.get_cliente_data, name="get-cliente-data"),

]
