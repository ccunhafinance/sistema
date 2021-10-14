import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from clients.models import Espelhamento
from users.models import CustomUser


main_icon = 'ni ni-users'

class ListViewClients(LoginRequiredMixin, generic.TemplateView):
    template_name = "clients/list_view.html"
    login_url = '/'


    def get_context_data(self, **kwargs):

        with open('data/clientes/clientes.txt', encoding='latin1') as json_file:
            clientes = json.load(json_file)

        context = {
            'clientes': clientes,
            # Crumbs First Page Config
            'first_page_name': 'Clientes',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Meus Clientes',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': '',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Clientes',
            'subtitle': 'Meus Clientes',
            'sticker': 'Novo',
            'page_description': 'Listagem de todos os meus clientes.'
        }

        return context

class ListMirrorView(LoginRequiredMixin, generic.TemplateView):
    template_name = "clients/mirror_view.html"
    login_url = '/'

    def get_context_data(self, **kwargs):

        with open('data/clientes/clientes.txt', encoding='latin1') as json_file:
            clientes = json.load(json_file)

        context = {
            'clientes': clientes,
            'espelhamento': Espelhamento.objects.all(),
            'usuarios': CustomUser.objects.filter(type='assessor'),
            # Crumbs First Page Config
            'first_page_name': 'Clientes',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Espelhamento',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': '',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Espelhamento',
            'subtitle': '',
            'sticker': 'Novo',
            'page_description': 'Listagem de clientes espelhados.'
        }

        return context

def mirroradd(request):
    if request.method == 'POST':
        data = Espelhamento(
            assessor=CustomUser.objects.get(id=request.user.id),
            assessor_permited=request.POST['assessor_permited']
        )

        data.save()

        return redirect(reverse('clients:mirror-list'))

def mirrordelete(request, pk):
    data = Espelhamento(
        id=pk,
    )
    data.delete()

    return redirect(reverse('clients:mirror-list'))

# Create your views here.
def get_cliente_data(request):
    with open('data/clientes/clientes.txt', encoding='latin1') as json_file:
        clientes = json.load(json_file)


    code = request.POST['code']

    response = []
    for cliente in clientes:
        if cliente['CODIGO_XP_ASSESSOR'] == int(code):

            response.append( '<tr>' \
                           '<td>'+ str(cliente['CODIGO_XP_CLIENTE']) + '</td>'\
                           '<td>'+ str(cliente['NOME_CLIENTE']) + '</td>'\
                           '<td>'+ '<a href="mailto:'+str(cliente['EMAIL_CLIENTE'])+'">'+str(cliente['EMAIL_CLIENTE'])+'</a>' + '</td>'\
                       '</th>')




    return HttpResponse(response)

