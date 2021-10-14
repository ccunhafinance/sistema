from django.urls import path
from .views import *

app_name = 'myzauth'

urlpatterns = [
    path('', MyLoginView.as_view(), name="login"),
    path('logout/', MyLogoutView.as_view(), name="logout"),
]