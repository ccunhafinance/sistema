from django.urls import path
from .views import *
from .import views

app_name = 'seguros'

urlpatterns = [
    # PAGINA principal
    path('', views.mainPageSeguro, name="seguro-main"),
]
