from django.urls import path
from .views import *
from .import views

app_name = 'ajax'

urlpatterns = [
    path('', views.get_client, name="get-client"),
    path('send-mail-ipo/', views.send_mail_ipo, name="send-mail-ipo"),
    path('get-mail-ipo/', views.get_mail_ipo, name="get-mail-ipo"),

    path('send-mail-rf/', views.send_mail_rf, name="send-mail-rf"),
    path('get-mail-rf/', views.get_mail_rf, name="get-mail-rf"),
]