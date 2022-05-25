import csv
from dataclasses import replace
from django.core.mail import EmailMessage
from googlefinance import getQuotes
import requests
from django.core.files.storage import FileSystemStorage
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
import xlrd
from collections import OrderedDict
import json
from clients.models import Espelhamento
from users.models import CustomUser
from .forms import *
import pandas as pd
from bs4 import BeautifulSoup as bs
import os
from pathlib import Path
from datetime import datetime, timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import time
import locale
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


# Gbobal Variables
main_icon = 'ni ni-tag'

# Ofertas de Renda Fixa (RF)
# --------------------------------------------------------------------------------

# Listar
class OfferRfListView(LoginRequiredMixin, generic.TemplateView):
    template_name = "offers/rf/list_view.html"
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = {
            'list_data': OfferRf.objects.all(),
            # Crumbs First Page Config
            'first_page_name': 'Ofertas',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Renda Fixa',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': '',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Ofertas (RF)',
            'subtitle': '',
            'sticker': 'Novo',
            'page_description': 'Listagem de todas as ofertas de Renda Fixa'
        }

        return context

# Adicionar
@login_required(login_url='/')
def createrf(request):

    order_forms = OfferRf()
    item_order_formset = inlineformset_factory(OfferRf, SerieRf, form=SeriesRfForm, extra=1, can_delete=True)

    if request.method == 'POST':
        forms = OfferRfForm(request.POST, request.FILES, instance=order_forms, prefix='main')
        formset = item_order_formset(request.POST, request.FILES, instance=order_forms, prefix='product')

        if forms.is_valid() and formset.is_valid():
            forms = forms.save(commit=False)
            forms.save()
            formset.save()
            return redirect(reverse('offers:listar-rf'))

    else:
        forms = OfferRfForm(instance=order_forms, prefix='main')
        formset = item_order_formset(instance=order_forms, prefix='product')

    context = {
        'forms': forms,
        'formset': formset,
        # Crumbs First Page Config
        'first_page_name': 'Ofertas',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Renda Fixa',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': 'Add',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Ofertas (RF)',
        'subtitle': 'Add',
        'sticker': 'Novo',
        'page_description': 'Formulário de cadastro de ofertas de Renda Fixa'
    }

    return render(request, 'offers/rf/create_view.html', context)

# Editar
@login_required(login_url='/')
def editrf(request, pk):

        order_forms = OfferRf.objects.filter(id=pk).first()
        item_order_formset = inlineformset_factory(OfferRf, SerieRf, form=SeriesRfForm, extra=0, can_delete=True)

        if order_forms is None:

            return redirect(reverse('offers:listar-rf'))

        if request.method == 'POST':
            forms = OfferRfForm(request.POST, request.FILES, instance=order_forms, prefix='main')
            formset = item_order_formset(request.POST, request.FILES, instance=order_forms, prefix='product')

            if forms.is_valid() and formset.is_valid():
                forms = forms.save(commit=False)
                forms.save()
                formset.save()
                return redirect(reverse('offers:listar-rf'))

        else:
            forms = OfferRfForm(instance=order_forms, prefix='main')
            formset = item_order_formset(instance=order_forms, prefix='product')


        context = {
            'forms': forms,
            'formset': formset,
            # Crumbs First Page Config
            'first_page_name': 'Ofertas',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Renda Fixa',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': 'Editar',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Ofertas (RF)',
            'subtitle': 'Editar',
            'sticker': '',
            'page_description': 'Formulário de edição de ofertas de Renda Fixa (' + order_forms.ativo + ' ' + order_forms.emissor + ')'
        }

        return render(request, 'offers/rf/edit_view.html', context)

# Enviar E-mail
@login_required(login_url='/')
def sendemailrf(request, pk):
    oferta = OfferRf.objects.get(id=pk)
    series = SerieRf.objects.filter(pk=oferta.id)

    hora = datetime.now()

    if hora.hour >= 6 and hora.hour < 12:
        saldacao = 'Bom dia'
    elif hora.hour > 12 and hora.hour < 18:
        saldacao = 'Boa tarde'
    else:
        saldacao = 'Boa noite'

    context = {
        'espelhamento': Espelhamento.objects.all(),
        'saldacao': saldacao,
        'oferta': oferta,
        'pk': pk,
        'series': series,
        # Crumbs First Page Config
        'first_page_name': 'Ofertas',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Renda Fixa',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': 'Enviar Email',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Ofertas (RF)',
        'subtitle': '',
        'sticker': '',
        'page_description': 'Formulário de envio de E-mail - Oferta: ' + oferta.ativo + ' ' + oferta.emissor
    }

    return render(request, 'offers/rf/email_view.html', context)

# Pagina Email enviado
@login_required(login_url='/')
def sentmailrf(request, id):
    context = {
        'email': EmailRf.objects.get(pk=id),
        # Crumbs First Page Config
        'first_page_name': 'Ofertas',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Renda Fixa',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': 'Vizualização do Email',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Ofertas (RF)',
        'subtitle': '',
        'sticker': '',
        'page_description': 'Vizualização do email de oferta enviada!'
    }

    return render(request, 'offers/rf/sent_email_view.html', context)

# Excluir
class DeleteOfferRfView(LoginRequiredMixin, generic.DeleteView):
    template_name = "offers/rf/delete_view.html"
    login_url = '/'

    queryset = OfferRf.objects.all()

    # def get_object(self):
    #     id_ = self.kwargs.get('id')
    #     return get_object_or_404(OfferRf, id=id_),

    # print(get_object)

    def get_success_url(self):
        return reverse("offers:listar-rf")

    def get_context_data(self, **kwargs):
        id_ = self.kwargs.get('pk')
        oferta = get_object_or_404(OfferRf, id=id_)
        context = {
            'object': oferta,
            # Crumbs First Page Config
            'first_page_name': 'Ofertas',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Renda Fixa',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': 'Excluir',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Ofertas (RF)',
            'subtitle': 'Excluir',
            'sticker': '',
            'page_description': 'Excluir oferta ('+oferta.ativo +' '+oferta.emissor+')'
        }

        return context

# Ofertas de Renda Variável (RV)
# --------------------------------------------------------------------------------

#  IPO
# --------------------------------------------------------------------------------

# Listar
class OfferRvIpoListView(LoginRequiredMixin, generic.TemplateView):
    template_name = "offers/rv/ipo/list_view.html"
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = {
            'list_data': OfferRvIpo.objects.all(),
            # Crumbs First Page Config
            'first_page_name': 'Ofertas',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Renda Variável',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': '',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Ofertas (RV)',
            'subtitle': 'IPO',
            'sticker': 'Novo',
            'page_description': 'Listagem de todas as ofertas de Renda Variável IPO'
        }

        return context

# Adicionar
@login_required(login_url='/')
def creatervipo(request):

    order_forms = OfferRvIpo()
    item_order_formset = inlineformset_factory(OfferRvIpo, ModalidadeIpo, form=ModalidadeIpoForm, extra=1, can_delete=True)

    if request.method == 'POST':
        forms = OfferRvIpoForm(request.POST, request.FILES, instance=order_forms, prefix='main')
        formset = item_order_formset(request.POST, request.FILES, instance=order_forms, prefix='product')

        if forms.is_valid() and formset.is_valid():
            forms = forms.save(commit=False)
            forms.save()
            formset.save()
            return redirect(reverse('offers:listar-rv-ipo'))

    else:
        forms = OfferRvIpoForm(instance=order_forms, prefix='main')
        formset = item_order_formset(instance=order_forms, prefix='product')

    context = {
        'forms': forms,
        'formset': formset,
        # Crumbs First Page Config
        'first_page_name': 'Ofertas',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Renda Variável',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': 'Add',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Ofertas (Rv)',
        'subtitle': 'IPO',
        'sticker': 'Novo',
        'page_description': 'Formulário de cadastro de ofertas de Renda Variável IPO'
    }

    return render(request, 'offers/rv/ipo/create_view.html', context)

# Editar
@login_required(login_url='/')
def editrvipo(request, pk):

        order_forms = OfferRvIpo.objects.filter(id=pk).first()
        item_order_formset = inlineformset_factory(OfferRvIpo, ModalidadeIpo, form=ModalidadeIpoForm, extra=0, can_delete=True)

        if order_forms is None:

            return redirect(reverse('offers:listar-rv-ipo'))

        if request.method == 'POST':
            forms = OfferRvIpoForm(request.POST, request.FILES, instance=order_forms, prefix='main')
            formset = item_order_formset(request.POST, request.FILES, instance=order_forms, prefix='product')

            if forms.is_valid() and formset.is_valid():
                forms = forms.save(commit=False)
                forms.save()
                formset.save()
                return redirect(reverse('offers:listar-rv-ipo'))

        else:
            forms = OfferRvIpoForm(instance=order_forms, prefix='main')
            formset = item_order_formset(instance=order_forms, prefix='product')


        context = {
            'forms': forms,
            'formset': formset,
            # Crumbs First Page Config
            'first_page_name': 'Ofertas',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Renda Variável',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': 'Editar',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Ofertas (Rv)',
            'subtitle': 'Editar',
            'sticker': '',
            'page_description': 'Formulário de edição de ofertas de Renda Fixa (' + order_forms.ticker + ' ' + order_forms.company + ')'
        }

        return render(request, 'offers/rv/ipo/edit_view.html', context)

# Deletar
class DeleteOfferRvIpoView(LoginRequiredMixin, generic.DeleteView):
    template_name = "offers/rv/ipo/delete_view.html"
    login_url = '/'

    queryset = OfferRvIpo.objects.all()

    # def get_object(self):
    #     id_ = self.kwargs.get('id')
    #     return get_object_or_404(OfferRf, id=id_),

    # print(get_object)

    def get_success_url(self):
        return reverse("offers:listar-rv-ipo")

    def get_context_data(self, **kwargs):
        id_ = self.kwargs.get('pk')
        oferta = get_object_or_404(OfferRvIpo, id=id_)
        context = {
            'object': oferta,
            # Crumbs First Page Config
            'first_page_name': 'Ofertas',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Renda Variável',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': 'Excluir',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Ofertas (RV) IPO',
            'subtitle': 'Excluir',
            'sticker': '',
            'page_description': 'Excluir oferta ('+oferta.ticker +' - '+oferta.company+')'
        }

        return context

# Enviar E-mail
@login_required(login_url='/')
def sendmailrvipo(request, pk):
    oferta = OfferRvIpo.objects.filter(id=pk).first()
    modalidades = ModalidadeIpo.objects.filter(pk=oferta.id)

    hora = datetime.now()

    if hora.hour >= 6 and hora.hour < 12:
        saldacao = 'Bom dia'
    elif hora.hour > 12 and hora.hour < 18:
        saldacao = 'Boa tarde'
    else:
        saldacao  = 'Boa noite'

    context = {
        'espelhamento': Espelhamento.objects.all(),
        'saldacao': saldacao,
        'oferta': oferta,
        'pk': pk,
        'modalidades': modalidades,
        # Crumbs First Page Config
        'first_page_name': 'Ofertas',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Renda Variável',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': 'Enviar Email',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Ofertas (RV)',
        'subtitle': 'IPO',
        'sticker': 'Novo',
        'page_description': 'Formulário de envio de E-mail - Oferta: '+ oferta.ticker +' '+oferta.company
    }

    return render(request, 'offers/rv/ipo/email_view.html', context)

# Pagina Email enviado
@login_required(login_url='/')
def sentmailrvviewipo(request, id):
    context = {
        'email': EmailIpo.objects.get(pk=id),
        # Crumbs First Page Config
        'first_page_name': 'Ofertas',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Renda Variável',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': 'Vizualização do Email',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Ofertas (RV)',
        'subtitle': 'IPO',
        'sticker': 'Novo',
        'page_description': 'Vizualização do email de oferta enviada!'
    }

    return render(request, 'offers/rv/ipo/sent_email_view.html', context)

# Direito de Subscrição
# --------------------------------------------------------------------------------

#  Listar
class OfferRvSubscriptionListView(LoginRequiredMixin, generic.TemplateView):
    template_name = "offers/rv/subscription/list_view.html"
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = {
            'list_view': OfferRvSubscription.objects.all(),
            # Crumbs First Page Config
            'first_page_name': 'Ofertas',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Renda Variável',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': '',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Ofertas (RV)',
            'subtitle': 'Direito de Subscrição',
            'sticker': 'Novo',
            'page_description': 'Listagem de todas as ofertas de Renda Variável Direito de Subscrição'
        }

        return context

# Adicionar
class OfferRvSubscriptionCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "offers/rv/subscription/create_view.html"
    form_class = SubscriptionForm
    # queryset = OfferRvSubscription.objects.all()
    login_url = '/'

    def get_success_url(self):
        return reverse("offers:listar-rv-subscription")

    def get_context_data(self, **kwargs):

        context = {
            'form': SubscriptionForm,
            # Crumbs First Page Config
            'first_page_name': 'Ofertas',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Renda Variável',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': '',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Ofertas (RV)',
            'subtitle': 'Direito de Subscrição',
            'sticker': 'Novo',
            'page_description': 'Listagem de todas as ofertas de Renda Variável Direito de Subscrição'
        }

        return context

# Editar
class OfferRvSubscriptionEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = "offers/rv/subscription/edit_view.html"
    form_class = SubscriptionForm
    login_url = '/'

    queryset = OfferRvSubscription.objects.all()

    def get_success_url(self):
        return reverse("offers:listar-rv-subscription")

    def get_context_data(self, **kwargs):

        id_ = self.kwargs.get('pk')
        oferta = get_object_or_404(OfferRvSubscription, id=id_)
        odd = OfferRvSubscription.objects.get(id=id_)
        form = SubscriptionForm(instance=odd)
        context = {
            'object': oferta,
            'form': form,
            # Crumbs First Page Config
            'first_page_name': 'Ofertas',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Renda Variável',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': 'Editar',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Ofertas (RV)',
            'subtitle': 'Direito de Subscrição',
            'sticker': 'Novo',
            'page_description': 'Listagem de todas as ofertas de Renda Variável Direito de Subscrição '+oferta.ticker+' '+oferta.company
        }

        return context

# Excluir
class OfferRvSubscriptionDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "offers/rv/subscription/delete_view.html"
    # form_class = SubscriptionForm
    login_url = '/'

    queryset = OfferRvSubscription.objects.all()

    def get_success_url(self):
        return reverse("offers:listar-rv-subscription")

    def get_context_data(self, **kwargs):
        id_ = self.kwargs.get('pk')
        oferta = get_object_or_404(OfferRvSubscription, id=id_)
        context = {
            'object': oferta,
            # Crumbs First Page Config
            'first_page_name': 'Ofertas',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Renda Variável',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': 'Excluir',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Ofertas (RV)',
            'subtitle': 'Direito de Subscrição',
            'sticker': 'Novo',
            'page_description': 'Listagem de todas as ofertas de Renda Variável Direito de Subscrição'
        }

        return context

def get_ticker_price(request):

    # ticker = 'TSLA34'
    ticker = request.POST['ticker']
    result = requests.get('https://www.google.com/finance/quote/'+ticker+':BVMF?hl=pt')
    src = result.content
    soup = bs(src, 'lxml')
    price = soup.find('div', attrs={'class': 'YMlKec fxKbKc'})
    data_site = soup.find('div', attrs={'class': 'ygUjEc'})

    if price == None:
        response = 'No'
    else:

        divide = data_site.text.split('.')
        pega_data = divide[0]
        pega_hora = divide[1].split('·')
        hora_final = pega_hora[0].split(' ')

        data_format = pega_data.split(' ')
        dia = data_format[0]
        mes = data_format[2]
        ano = datetime.now().year

        nova_data = str(mes) + ' '+ str(dia) + ' '+ str(ano)

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        # from_date="mar 15 2010"
        conv=time.strptime(nova_data,"%b %d %Y")
        data_convertida = time.strftime("%Y-%m-%d",conv)
        # print(data_convertida)
        # print(hora_final[1])

        response =     '<input hidden id="price_goo" value="'+price.text+'">' \
                       '<input hidden id="date_goo" value="'+data_convertida+'">' \
                       '<input hidden id="time_goo" value="'+hora_final[1]+'">' \
                      
    
    return HttpResponse(response)

# FII

# --------------------------------------------------------------------------------

# Listar
@login_required(login_url='/')
def ofertarvfiiview(request):
        # users_in_group = Group.objects.all()
        #
        # if user in users_in_group:
        #     print()


        # diretorio = Path('data/ofertas/fii/')
        # arquivo = diretorio / 'ticker11_data.json'

        # stat_result = arquivo.stat()
        # last_update = datetime.fromtimestamp(stat_result.st_mtime, tz=None)

        # with open('data/ofertas/fii/ticker11_data.json') as json_file:
        #     ticker11 = json.load(json_file)

        # the_ticker = []
        # for ticker in ticker11:
        #     soup = bs(ticker['ticker'], 'lxml')
        #     text = soup.get_text()
        #     if os.path.isfile('data/ofertas/fii/subscricao/' + text + '.json'):
        #         new_ticker = ticker['ticker']

        #         with open('data/ofertas/fii/subscricao/'+text+'.json') as json_file:
        #             subs = json.load(json_file)

        #             teste = []

        #             for sub in subs:
        #                 if str(request.user.codigo) == str(sub['CodAssessor'].replace('A', '')):
        #                     teste.append(sub['CodigoCliente'])

        #             if len(teste) > 0:
        #                 the_ticker.append(ticker)

        # # print(the_ticker)

        # if CustomUser.objects.filter(pk=request.user.id, groups__name='Área de Alocação').exists():
        #     filtered_offers_by_group = ticker11[:-10]
        #     quem = True
        # else:
        #     filtered_offers_by_group = the_ticker
        #     quem = False

        scope = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name('data/apis_google/client_key.json', scope)
        client = gspread.authorize(creds)

        sheet = client.open('Emissão FII')

        sheet_instance = sheet.get_worksheet(0)
       
        records_data = sheet_instance.get_all_records()


        context = {
            # 'ofertas': filtered_offers_by_group,
            # 'last_update': last_update,
            'googleForm': FiiForm,
            'ofertas': records_data,
            # 'quem': quem,
            # Crumbs First Page Config
            'first_page_name': 'Ofertas',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Renda Variável',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': '',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Ofertas (RV)',
            'subtitle': 'Fundos Imobiliários (Fii)',
            'sticker': 'Novo',
            'page_description': 'Listagem de todas as ofertas de Renda Variável de Fundos Imobiliários.'
        }


        return render(request, 'offers/rv/fii/list_view.html', context)
# ADD FII GOOOGLE SHETS
def addFii(request):
    scope = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
        ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('data/apis_google/client_key.json', scope)
    client = gspread.authorize(creds)

    sheetadd = client.open('Emissão FII').sheet1
    row = [
            
            '-',
            request.POST.get('fundo', False),
            request.POST.get('emissao', False),
            request.POST.get('preco', False),
            request.POST.get('cotacao', False),
            request.POST.get('data_base', False),
            request.POST.get('periodo_de_negociacao_inicial', False),
            request.POST.get('periodo_de_negociacao_final', False),
            request.POST.get('periodo_de_preferencia_inicial', False),
            request.POST.get('periodo_de_preferencia_final', False),
            request.POST.get('periodo_de_sobras_inicial', False),
            request.POST.get('periodo_de_sobras_final', False),
            request.POST.get('perio_do_publico_inicial', False),
            request.POST.get('perio_do_publico_final', False),
            request.POST.get('prospecto', False),
            request.POST.get('tipo_de_oferta', False),
            request.POST.get('preco_e_taxa', False),
            request.POST.get('data_encerramento', False),
            request.POST.get('proporcao_de_preferencia', False),
            request.POST.get('proporcaode_sobras', False),
            request.POST.get('investimento_minimo', False),
            request.POST.get('captacao_minima', False),
            request.POST.get('captacao_maxima', False),
            request.POST.get('coordenador_lider', False),
            request.POST.get('data_de_encerramento', False),
            request.POST.get('metodo_de_rateio', False),
            request.POST.get('resultado_do_rateio', False),
            
    ]
    index = 2
    sheetadd.insert_row(row, index)

    return redirect('/ofertas/rv/fii/listar/')

@login_required(login_url='/')
def sendemailrvfii(request, id, ticker):

    result = requests.get('https://www.google.com/finance/quote/'+ticker+':BVMF?hl=pt')
    src = result.content
    soup = bs(src, 'lxml')
    price = soup.find('div', attrs={'class': 'YMlKec fxKbKc'})
    data_site = soup.find('div', attrs={'class': 'ygUjEc'})
    divide = data_site.text.split('.')
    pega_data = divide[0]
    pega_hora = divide[1].split('·')
    hora_final = pega_hora[0].split(' ')

    data_format = pega_data.split(' ')
    dia = data_format[0]
    mes = data_format[2]
    ano = datetime.now().year

    nova_data = str(mes) + ' '+ str(dia) + ' '+ str(ano)

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    conv=time.strptime(nova_data,"%b %d %Y")
    data_convertida = time.strftime("%Y-%m-%d",conv)
  
    with open('data/ofertas/fii/ticker11_data.json') as json_file:
        ticker11 = json.load(json_file)

    with open('data/ofertas/fii/subscricao/' + ticker + '.json') as json_file:
        subs = json.load(json_file)

    a_oferta = []
    for oferta in ticker11:
        if str(oferta['id']) == str(id):
            a_oferta = oferta

    hora = datetime.now()

    if hora.hour >= 6 and hora.hour < 12:
        saldacao = 'Bom dia'
    elif hora.hour > 12 and hora.hour < 18:
        saldacao = 'Boa tarde'
    else:
        saldacao = 'Boa noite'

    data_convertida = datetime.strptime(data_convertida, '%Y-%m-%d')

    context = {
        'espelhamento': Espelhamento.objects.all(),
        'preco_merc': price.text,
        'data_merc': data_convertida,
        'hora_merc': hora_final[1],
        'oferta': a_oferta,
        'saldacao': saldacao,
        'ticker': ticker,
        'clientes': subs,
        'registro_email' : RegisttoEmailFii.objects.filter(ticker=ticker),
        # Crumbs First Page Config
        'first_page_name': 'Ofertas',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Renda Variável',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': 'Enviar Email',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Ofertas (RV)',
        'subtitle': 'Fii',
        'sticker': '',
        'page_description': 'Formulário de envio de E-mail FII' 
    }

    return render(request, 'offers/rv/fii/email_view.html', context)

@login_required(login_url='/')
def envia_email_fii(request):

    id_oferta = request.POST['id_oferta']
    ticker = request.POST['ticker']

    qtd = request.POST['qtd']
    preco_oferta = request.POST['preco_oferta']
    preco_mercado = request.POST['preco_merc']
    data_preco_mercado = request.POST['data_merc']
    remetente = request.POST['remetente']
    codigo_cliente = request.POST['form_cod_cliente']

    enviado_por = request.POST['enviado_por']
    assunto = request.POST['assunto']
    corpo_email = request.POST['corpo_email']
    emaildocliente = [request.POST['emaildocliente']]

    responder_a = CustomUser.objects.get(id=enviado_por).email
    enviar_para = [request.POST['emailteste']]
    # enviar_para = [emaildocliente]

    email = EmailMessage(
        assunto,
        corpo_email,
        'Inove Investimentos <web@inoveinvestimentos.com.br>',
        enviar_para,
        reply_to=[responder_a],
        headers={'Message-ID': 'foo'},
    )
    email.content_subtype = "html"
    email.send()

    preco_oferta = preco_oferta.replace('R$','')
    preco_oferta = preco_oferta.replace(',','.')
    preco_mercado = preco_mercado.replace('R$','')
    preco_mercado = preco_mercado.replace(',','.')

    registro_email_fii = RegisttoEmailFii(
        ticker=ticker ,
        cliente=codigo_cliente,
        enviado_por=enviado_por,
        remetente=remetente,
        email=request.POST['emaildocliente'],
        preco_mercado= float(preco_mercado),
        data_prec_mercado=datetime.strptime(data_preco_mercado, '%Y-%m-%d'),
        preco_oferta=float(preco_oferta),
        conteudo_email=corpo_email,
        quantidade=qtd ,
    ) 

    registro_email_fii.save()

    

    # Redirect to same page after form submit
    return redirect('/ofertas/rv/fii/enviar-email-rv-fii/'+id_oferta+'/'+ticker)

# Scrape TICKER11
@login_required(login_url='/')
def scrapy_ticker11(request):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    # US english
    LANGUAGE = "pt-br"

    url ='https://docs.google.com/spreadsheets/d/e/2PACX-1vTDOrguvv8Ng5o6YUK_oUR82u-K-qi5ZGD42punDkkssagSgeqIYpXKwOlXZce_pSWY06fUNUBLREsF/pubhtml?gid=0&single=true'

    def get_soup(url):
        """Constructs and returns a soup using the HTML content of `url` passed"""
        # initialize a session
        session = requests.Session()
        # set the User-Agent as a regular browser
        session.headers['User-Agent'] = USER_AGENT
        # request for english content (optional)
        session.headers['Accept-Language'] = LANGUAGE
        session.headers['Content-Language'] = LANGUAGE
        # make the request
        html = session.get(url)
        # return the soup
        return bs(html.content, "html.parser")

    def get_all_tables(soup):
        """Extracts and returns all tables in a soup object"""
        return soup.find_all("table")

    def get_table_headers(table):
        """Given a table soup, returns all the headers"""
        headers = ["ticker",'id',"icvm","totaldecotas","valorminimo","cotacao","cotacaooferta","preferencia","negociaveil","datacom","Dinicio","Dtermino","Dliquidacao","Finicio","Ftermino","Fliquidacao","Pinicio","Ptermino","Pliquidacao"]
        # for th in table.find("tr").find_all("th"):
        #     headers.append(th.text.strip())
        return headers

    def get_table_rows(table):
        """Given a table, returns all its rows"""
        rows = []
        a = 0
        for tr in table.find_all("tr")[1:]:
            cells = []
            # grab all td tags in this table row
            tds = tr.find_all("td")
            if len(tds) == 0:
                # if no td tags, search for th tags
                # can be found especially in wikipedia tables below the table
                ths = tr.find_all("th")
                for th in ths:

                    cells.append(th.text.strip())
                    
            else:
                # use regular td tags
                for td in tds:
                    
                    if td.find("a"):
                        
                        cells.append(td)
                    else:
                        cells.append(td.text.strip())
            rows.append(cells)
            a += 1

        rows = rows[4:]

        return rows

    def save_as_csv(table_name, headers, rows):
        path = 'data/ofertas/fii'
        pd.DataFrame(rows, columns=headers).to_csv(os.path.join(path, f"{table_name}.csv"))

    def csv_to_json(csvFilePath, jsonFilePath):
        jsonArray = []

        # read csv file
        with open(csvFilePath, encoding='utf-8') as csvf:
            # load csv file data using csv library's dictionary reader
            csvReader = csv.DictReader(csvf)

            # convert each csv row into python dict
            a=0
            for row in csvReader:
                if row['id'] == '':
                    row['id'] = str(a)
                
                # add this python dict to json array
                jsonArray.append(row)
                a += 1
        
        # convert python jsonArray to JSON String and write to file
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            jsonString = json.dumps(jsonArray, indent=4)
            jsonf.write(jsonString)


    # get the soup
    soup = get_soup(url)
    # extract all the tables from the web page
    tables = get_all_tables(soup)
    print(f"[+] Found a total of {len(tables)} tables.")
    # iterate over all tables
    for i, table in enumerate(tables, start=1):
        # get the table headers
        # removetable = str.maketrans('', '', '@#%-?/()$ ')
        headers = get_table_headers(table)
        # headers = [s.translate(removetable) for s in headers]
        # print(headers)
        # get all the rows of the table
        rows = get_table_rows(table)
        # save table as csv file
        table_name = f"table-{i}"
        print(f"[+] Saving {table_name}")
        save_as_csv(table_name, headers, rows)

        csvFilePath = r'data/ofertas/fii/table-1.csv'
        jsonFilePath = r'data/ofertas/fii/ticker11_data.json'
        csv_to_json(csvFilePath, jsonFilePath)

    return redirect('/ofertas/rv/fii/listar/')

@login_required(login_url='/')
def fii_files_upload(request):

    if request.method == 'POST':
        f=request.FILES['file']
        fs = FileSystemStorage(location='data/ofertas/fii/subscricao/')
        # fs.path('data/ofertas/fii/subscription/')
        fs.save(str(request.POST['ticker']+'.xlsx'), f)

        wb = xlrd.open_workbook('data/ofertas/fii/subscricao/'+str(request.POST['ticker']+'.xlsx'))
        sh = wb.sheet_by_index(0)


        data_list = []

        for rownum in range(1, sh.nrows):
            data = OrderedDict()

            row_values = sh.row_values(rownum)
            data['CodigoCliente'] = row_values[0]
            data['IdEvento'] = row_values[1]
            data['DataDebito'] = row_values[2]
            data['DataEx'] = row_values[3]
            data['DataUltimoDiaNegociacao'] = row_values[4]
            data['Proporcao'] = row_values[5]
            data['QuantidadeExercida'] = row_values[6]
            data['AEfetivar'] = row_values[7]
            data['QuantidadeRequerida'] = row_values[8]
            data['IdSolicitacao'] = row_values[9]
            data['DataSolicitacao'] = row_values[10]
            data['UsuarioSolicitante'] = row_values[11]
            data['Status'] = row_values[12]
            data['QuantidadeSolicitada'] = row_values[13]
            data['ErroBolsa'] = row_values[14]
            data['QuantidadeDisponivel'] = row_values[15]
            data['QuantidadeAdicionalSolicitada'] = row_values[16]
            data['QuantidadeAdicionalExercida'] = row_values[17]
            data['ValorDireito'] = row_values[18]
            data['CodNegociacao'] = row_values[19]
            data['Marca'] = row_values[20]
            data['NomeFilial'] = row_values[21]
            data['CodAssessor'] = row_values[22]
            data_list.append(data)

        with open('data/ofertas/fii/subscricao/'+str(request.POST['ticker']+'.json'), "w", encoding="utf-8") as writeJsonfile:
            json.dump(data_list, writeJsonfile, indent=4, default=str)


        fs.delete(str(request.POST['ticker'] + '.xlsx'))
        
        return HttpResponse('s')
    else:
        return HttpResponse('uploaded')

# FII EDIT

# Adicionar
class OfferRvFiiCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "offers/rv/fii/edit/create_view.html"
    form_class = FiiEditForm
    # queryset = OfferRvSubscription.objects.all()
    login_url = '/'

    def get_success_url(self):
        return reverse("offers:listar-rv-fii")

    def get_context_data(self, **kwargs):
        context = {
            'form': FiiEditForm,
            # Crumbs First Page Config
            'ticker': self.kwargs['ticker'],
            'emissor': self.kwargs['emissor'],

            'first_page_name': 'Ofertas',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Renda Variável',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': '',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Ofertas (RV)',
            'subtitle': 'Direito de Subscrição',
            'sticker': 'Novo',
            'page_description': 'Adicionar Edit Fii'
        }

        return context

# Editar
class OfferRvFiiEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = "offers/rv/fii/edit/edit_view.html"
    form_class = FiiEditForm
    login_url = '/'

    queryset = FiiEdit.objects.all()

    def get_success_url(self):
        return reverse("offers:listar-rv-fii")

    def get_context_data(self, **kwargs):

        id_ = self.kwargs.get('pk')
        oferta = get_object_or_404(FiiEdit, id=id_)
        odd = FiiEdit.objects.get(id=id_)
        form = FiiEditForm(instance=odd)
        context = {
            'object': oferta,
            'form': form,
            # Crumbs First Page Config
            'first_page_name': 'Ofertas',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Renda Variável',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': 'Editar',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Ofertas (RV)',
            'subtitle': 'Direito de Subscrição',
            'sticker': 'Novo',
            'page_description': 'Editar Fii'
        }

        return context

# Excluir
class OfferRvFiiDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "offers/rv/fii/edit/delete_view.html"
    # form_class = SubscriptionForm
    login_url = '/'

    queryset = FiiEdit.objects.all()

    def get_success_url(self):
        return reverse("offers:listar-rv-fii")

    def get_context_data(self, **kwargs):
        id_ = self.kwargs.get('pk')
        oferta = get_object_or_404(FiiEdit, id=id_)
        context = {
            'object': oferta,
            # Crumbs First Page Config
            'first_page_name': 'Ofertas',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Renda Variável',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': 'Excluir',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Ofertas (RV)',
            'subtitle': 'Direito de Subscrição',
            'sticker': 'Novo',
            'page_description': 'Excluir Edit Fii'
        }

        return context

# Scrape ClubeFii
@login_required(login_url='/')
def scrapy_clubefii(request):
    pass







