from django.urls import path
from .views import *

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboardView, name="dashboard"),
    path('teste/', views.teste, name="teste")

]