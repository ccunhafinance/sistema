from django.urls import path
from .views import ListViewAssessores

app_name = 'appname'

urlpatterns = [
         path('', ListViewAssessores.as_view(), name="assessores-list"),

]
