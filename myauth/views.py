from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView


class MyLoginView(LoginView):
    template_name = 'myauth/login.html'
    redirect_authenticated_user = True


class MyLogoutView(LogoutView):
    pass