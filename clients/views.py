import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from clients.models import Espelhamento
from users.models import CustomUser

from .models import Clientes
from .resources import ClientesResources
from django.contrib import messages
from tablib import Dataset
from datetime import date
import datetime

main_icon = 'ni ni-users'

def delet_all(request):
    clientes = Clientes.objects.all()

    for cliente in clientes:

        data = Clientes(id=cliente.id)
        data.delete()

    return redirect(reverse('clients:clients-list'))

def update_troca_assessor(request):
    rotina = request.POST.get('rotina', False)

    if rotina != False:
        rotina = '1'
    else:
        rotina = '0'

    data_atual = datetime.datetime.now()
    data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        rotina=rotina,
        zap_mail=request.POST['zap_mail'],
        status='ok',
        troca='ok',
        data_registro=data_em_texto

    )

    return redirect(reverse('clients:clients-list'))

def update_new_cliente(request):
    rotina = request.POST.get('rotina', False)

    if rotina != False:
        rotina = '1'
    else:
        rotina = '0'

    data_atual = datetime.datetime.now()
    data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        nome=request.POST['nome'],
        sexo=request.POST['sexo'],
        email=request.POST['email'],
        telefone=request.POST['telefone'],
        data_nascimento=request.POST['data_nascimento'],
        rotina=rotina,
        zap_mail=request.POST['zap_mail'],
        status='ok',
        data_registro=data_em_texto

    )

    return redirect(reverse('clients:clients-list'))

def upload_clientes(request):
    if request.method == 'POST':
        clientes_resource = ClientesResources()
        dataset = Dataset()
        new_cliente = request.FILES['myfile']

        if not new_cliente.name.endswith('xlsx'):
            messages.info('Formato de arquivo não suportado')
            return redirect(reverse('clients:clients-list'))

        imported_data = dataset.load(new_cliente.read(), format='xlsx')

        clientes = Clientes.objects.all()

        data_atual =  datetime.datetime.now()
        data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

        # print (len(clientes))

        if len(clientes)==0:

            for data in imported_data:

                try:
                    listing = Clientes.objects.get(nickname=data[1])

                except Clientes.DoesNotExist:
                    value = Clientes(
                        nickname=data[1],
                        nome=data[2],
                        sexo=data[3],
                        email=data[4],
                        telefone=data[5],
                        assessor=data[6],
                        data_nascimento=data[7],
                        data_registro=data_em_texto
                    )
                    value.save()

        else:

            t = len(imported_data)
            a = 0
            primeiro =[]
            segundo = []

            for cliente in clientes:

                primeiro.append(str(cliente.nickname))

                if a < t:
                    segundo.append(str(imported_data[a][0]))

                a += 1

            def Diff(li1, li2):
                return list(set(li1) - set(li2))

            # Inativa Cliente
            print(Diff(primeiro, segundo))

            inativos = Diff(primeiro, segundo)

            for x in inativos:
                Clientes.objects.filter(nickname=x).update(
                    status='Inativo',
                    data_registro=data_em_texto
                )

            for data in imported_data:

                if len(Clientes.objects.filter(nickname=data[0])) == 1:

                    if str(Clientes.objects.filter(nickname=data[0])[0].assessor) != str(data[2]):
                        Clientes.objects.filter(nickname=data[0]).update(
                            nome=data[1],
                            assessor=data[2],
                            antigo_assessor=Clientes.objects.filter(nickname=data[0])[0].assessor,
                            d0=data[3],
                            d1=data[4],
                            d2=data[5],
                            d3=data[6],
                            d4=data[7],
                            troca='existe',
                            data_registro=data_em_texto
                        )
                    else:

                        Clientes.objects.filter(nickname=data[0]).update(
                            nome=data[1],
                            d0=data[3],
                            d1=data[4],
                            d2=data[5],
                            d3=data[6],
                            d4=data[7],
                            data_registro=data_em_texto
                        )


                else:
                    value = Clientes(
                        nickname=data[0],
                        nome=data[1],
                        assessor=data[2],
                        d0=data[3],
                        d1=data[4],
                        d2=data[5],
                        d3=data[6],
                        d4=data[7],
                        status='Novo',
                        data_registro=data_em_texto
                    )
                    value.save()

    return redirect(reverse('clients:clients-list'))


class ListViewClients(LoginRequiredMixin, generic.TemplateView):
    template_name = "clients/list_view.html"
    login_url = '/'


    def get_context_data(self, **kwargs):

        # Load Clients based on the internal files
        # with open('data/clientes/clientes.txt', encoding='latin1') as json_file:
        #     clientes = json.load(json_file)

        # load Clients from DB

        clientes = Clientes.objects.all()
        n_clientes = len(clientes)
        novos_clientes = Clientes.objects.filter(status='Novo')
        inativo = Clientes.objects.filter(status='Inativo')
        n_inativo = len(inativo)
        n_novos_clientes = len(novos_clientes)

        i = Clientes.objects.filter(troca='existe')

        num_clientes_ativos = int(len(clientes)) - int(len(inativo))

        troca = len(i)

        context = {
            'clientes': clientes,
            'n_clientes': n_clientes,
            'inativo': inativo,
            'n_inativo': n_inativo,
            'novos_clientes': novos_clientes,
            'n_novos_clientes': n_novos_clientes,
            'n_troca_assessor': troca,
            'troca_assessor': i,
            'num_clientes_ativos': num_clientes_ativos,
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

