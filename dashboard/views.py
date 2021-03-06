from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .tasks import *

# Gbobal Variables
main_icon = 'ni ni-grid'

# Load Views
class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "dashboard/base.html"
    login_url = '/'


    def get_context_data(self, **kwargs):
        context = {
            # Crumbs First Page Config
            'first_page_name': 'Dashaboard',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': '',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': '',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Dashboard',
            'subtitle': 'Painel de Controles',
            'sticker': '',
            'page_description': ''
        }

        return context


def teste(request):
    # sleepy.delay(10)
    send_email_teste.delay()
    return HttpResponse('Emails Enviados!')