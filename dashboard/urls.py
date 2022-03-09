from django.urls import path
from .views import DashboardView

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('teste/', views.teste, name="teste")

]