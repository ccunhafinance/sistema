from django.urls import path

from chat import views

app_name = 'appname'

urlpatterns = [
    path('', views.messages_view, name="messages-view"),

]
