# from asyncio.windows_events import NULL
import json

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
import numpy
from requests import request
from clients.models import Espelhamento, NovoEmail, RegistroAtividades
from users.models import CustomUser, UserProfile
from .models import Clientes
from mail.models import *
from .resources import ClientesResources
from django.contrib import messages
from tablib import Dataset
from datetime import date
from datetime import timedelta, date
import datetime
from django.db import transaction
from .tasks import *
from django.http import JsonResponse
import datetime
import pandas as pd
from .tasks import *
import pytz
import datetime
import time
from django.conf import settings
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import xlrd


# FUNCAO PARA INSERIR NOVOS CLIENTES (INTERNO, EXTERNO)
def googleSheetsINEX(table, codigo,sexo,nome,email):
    scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]

    if sexo == 'F':
        tratamento = 'bem-vinda'
    else:
        tratamento = 'bem-vindo'

    creds = ServiceAccountCredentials.from_json_keyfile_name('data/apis_google/client_key.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(table).sheet1
    row = [codigo,tratamento,nome.split().pop(0),'emaildocis@gmail.com']
    index = 2
    sheet.insert_row(row, index)
# ----------------------------------------------------------------

def ctodatetime(ctimeinput):
    # etime = time.ctime(int(ctimeinput))
    btime = datetime.datetime.strptime(ctimeinput, "%a %b %d %H:%M:%S %Y")
    tz_aware_datetetime = btime.replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
    print(tz_aware_datetetime)
    return tz_aware_datetetime

main_icon = 'ni ni-users'
# ---------------------

def getMyClients(request):
    clients = []
    for cliente in Clientes.objects.filter(assessor=str(request.user.codigo)):

        if cliente.data_nascimento:
            nascimento = cliente.data_nascimento.strftime('%d/%m/%Y')
        else:
            nascimento = '0'

        if cliente.rotina:
            rotina = cliente.rotina
        else:
            rotina = '-'


        clients.append([cliente.nickname, cliente.nome,cliente.sexo,cliente.email,cliente.telefone,nascimento, rotina])
        

    return JsonResponse({"data": clients})

# ---------------------

def google_sheets(request):
    UserProfile.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        google_sheets=request.POST['google_sheets']
    )

    return redirect(reverse('clients:clients-onboarding'))

def delet_all(request):
    clientes = Clientes.objects.all()

    for cliente in clientes:

        data = Clientes(id=cliente.id)
        data.delete()

    return redirect(reverse('clients:clients-list'))

def update_troca_assessor_externo(request):
    rotina = request.POST.get('rotina', False)
    id = request.POST['id']

    if rotina != False:
        rotina = True

    Clientes.objects.filter(id=id).update(
        id=id,
        nome=request.POST['nome'],
        sexo=request.POST['sexo'],
        email=request.POST['email'],
        telefone=request.POST['telefone'],
        data_nascimento=request.POST['data_nascimento'],
        rotina=rotina,
        cliente_dia=True,
        alldone=True,
    )

    googleSheetsINEX('Indicação Cliente Onboarding',Clientes.objects.get(id=id).nickname, request.POST['sexo'],request.POST['nome'],request.POST['email'])

    if rotina == True:

        ClientsOnbording(
                cliente=Clientes.objects.get(id=id),
                email=False,
                frequencia_contato='Não Definido',
                meio_contato='Não Definido',
                assessor=request.POST['assessor'],
                perfil_preenchido=None,
                acomp_permanente=False,
                oportunidade_rf=False,
                oportunidade_acoes=False,
                oportunidade_fii=False,
                oportunidade_fundos=False,
                sujestao=None,
                alocacao=None,
                obs=''
            ).save()

    return redirect(reverse('clients:clients-onboarding'))
    
def update_troca_assessor(request):
    rotina = request.POST.get('rotina', False)
    id = request.POST['id']

    if rotina != False:
        rotina = True

    Clientes.objects.filter(id=id).update(
        id=id,
        nome=request.POST['nome'],
        rotina=rotina,
        cliente_dia=True,
        alldone=True,
    )

    googleSheetsINEX('Indicação Cliente Onboarding',Clientes.objects.get(id=id).nickname, Clientes.objects.get(id=id).sexo, request.POST['nome'],Clientes.objects.get(id=id).email)

    if rotina == True:

        ClientsOnbording(
                cliente=Clientes.objects.get(id=id),
                email=False,
                frequencia_contato='Não Definido',
                meio_contato='Não Definido',
                assessor=request.POST['assessor'],
                perfil_preenchido=None,
                acomp_permanente=False,
                oportunidade_rf=False,
                oportunidade_acoes=False,
                oportunidade_fii=False,
                oportunidade_fundos=False,
                sujestao=None,
                alocacao=None,
                obs=''
            ).save()

    # id_categ = Categoria.objects.first()
    # emailCateg = EmailCategoria.objects.filter(EmailCategoria_id=id_categ)
    # dias = date.today() + timedelta(days=0)
    # for a in emailCateg:
    #     value = NovoEmail(
    #         cliente_id=request.POST['id'],
    #         id_email=a.id,
    #         categ_email_id=id_categ.id,
    #         data_futuro=dias,
    #         status='n'

    #     )
    #     value.save()

    #     dias = dias + timedelta(days=7)

    return redirect(reverse('clients:clients-onboarding'))

def update_new_cliente(request):
    rotina = request.POST.get('rotina', False)
    id = request.POST['id']

    if rotina != False:
        rotina = True

    Clientes.objects.filter(id=id).update(
        id=id,
        nome=request.POST['nome'],
        sexo=request.POST['sexo'],
        email=request.POST['email'],
        telefone=request.POST['telefone'],
        data_nascimento=request.POST['data_nascimento'],
        rotina=rotina,
        cliente_dia=True,
        alldone=True,
    )

    googleSheetsINEX('Novos Clientes Onboarding',Clientes.objects.get(id=id).nickname, request.POST['sexo'],request.POST['nome'],request.POST['email'])
    
    if rotina == True:

        ClientsOnbording(
                cliente=Clientes.objects.get(id=id),
                email=False,
                frequencia_contato='Não Definido',
                meio_contato='Não Definido',
                assessor=request.user.codigo,
                perfil_preenchido=None,
                acomp_permanente=False,
                oportunidade_rf=False,
                oportunidade_acoes=False,
                oportunidade_fii=False,
                oportunidade_fundos=False,
                sujestao=None,
                alocacao=None,
                obs=''
            ).save()

    

    return redirect(reverse('clients:clients-onboarding'))

@transaction.atomic
def upload_clientes(request):

    if request.method == 'POST':
        new_cliente = request.FILES['myfile']
        xls = pd.ExcelFile(new_cliente)

        if not new_cliente.name.endswith('xlsx'):
            messages.info('Formato de arquivo não suportado')
            return redirect(reverse('clients:clients-list'))
  
    # ---------- Clientes
    clientes = Clientes.objects.all()

    assessores_clientes = []
    for cliente in clientes:
        assessores_clientes.append(cliente.assessor)

    if len(clientes) == 0:

        first_base = pd.read_excel(xls).to_numpy()

        clients_first_upload = []
        for data in first_base:

            data[7]
            replacement = data[7]
            s = data[1].split()
            s[0] = replacement
            nome_atualiazado = ' '.join(s)


            # print(birth)
            xl_date = data[6]

            datetime_date = xlrd.xldate_as_datetime(xl_date, 0)
            date_object = datetime_date.date()
            string_date = date_object.isoformat()

            value = Clientes(
                    nickname=data[0],
                    nome=str(nome_atualiazado).title(),
                    assessor=data[2],
                    sexo=data[3],
                    email=data[4],
                    telefone=data[5],
                    data_nascimento=string_date
                )
            clients_first_upload.append(value)
        Clientes.objects.bulk_create(clients_first_upload)

    if len(clientes) > 0:
        pass
        df1 = pd.read_excel(xls, 'tab2')
        df2 = pd.read_excel(xls, 'tab1')
        segundo_upload.apply_async((df1.to_json(), df2.to_json()), kwargs='')
       
    return redirect(reverse('clients:clients-list'))

@transaction.atomic
def teste_insert(request):

    clientes = Clientes.objects.all()

    if request.method == 'POST':
        new_cliente = request.FILES['myfile']
        xls = pd.ExcelFile(new_cliente)

        if not new_cliente.name.endswith('xlsx'):
            messages.info('Formato de arquivo não suportado')
            return redirect(reverse('clients:clients-list'))

        else:
            
            if len(clientes)==0:
                
                primeiro = pd.read_excel(xls) 
                upload_novos_clientes(primeiro.to_json()) #no deley
            else:
                df1 = pd.read_excel(xls, 'tab2')
                df2 = pd.read_excel(xls, 'tab1')
                segundo_upload(df1.to_json(),df2.to_json()) #no deley

    return redirect(reverse('clients:clients-list'))

# funcoes ombording

def updateOnbording(request):

    id = request.POST['id']
    name = request.POST['name']
    choice = request.POST['choice']

    response= ''

    # FREQUENCIA DE CONTATO ---------------------------------------------------------
    if name == 'frequenciaContato':
        ClientsOnbording.objects.filter(cliente_id=id).update(
            frequencia_contato=choice,
        )

        RegistroAtividades(
            cliente_id=Clientes.objects.get(id=id).id,
            registro='Frequencia de contato alterada!',
            descricao=choice,
            assessor_responsavel=request.user.id
        ).save()

        response = 'Frequencia de contato alterada para : <br>'+choice

    # PERFIL PREENCHIDO --------------------------------------------------------- 
    if name == 'perfilPreenchido':
        ClientsOnbording.objects.filter(cliente_id=id).update(
            perfil_preenchido=str(datetime.datetime.now()),
        )

        RegistroAtividades(
            cliente_id=Clientes.objects.get(id=id).id,
            registro='Perfil preenchido!',
            descricao=str(datetime.datetime.now()),
            assessor_responsavel=request.user.id
        ).save()

        response = 'O perfil foi preenchido na data de : <br>'+str(datetime.datetime.now())

    # MEIO DE CONTATO---------------------------------------------------------
    if name == 'meioDeContato':
        ClientsOnbording.objects.filter(cliente_id=id).update(
            meio_contato=choice,
        )

        RegistroAtividades(
            cliente_id=Clientes.objects.get(id=id).id,
            registro='Meio de Contato alterado!',
            descricao=choice,
            assessor_responsavel=request.user.id
        ).save()

        response = 'Meio de Contato alterado para :'+choice

    # ACOMPANHAMENTO PERMANENTE  ---------------------------------------------------------
    if name == 'acompanhamentoPermanente':
        check = ClientsOnbording.objects.get(cliente_id=id).acomp_permanente

        print(check)

        if check == True:
            choice = False
        else:
            choice = True

        ClientsOnbording.objects.filter(cliente_id=id).update(
            acomp_permanente=choice,
        )

        RegistroAtividades(
            cliente_id=Clientes.objects.get(id=id).id,
            registro='Acompanhamento Permanente alterado!',
            descricao=choice,
            assessor_responsavel=request.user.id
        ).save()

        response = 'Acompanhamento Permanente alterado para : <br>'+str(choice)

    # SUJESTAO ENVIADA ---------------------------------------------------------
    if name == 'sugestao':
        ClientsOnbording.objects.filter(cliente_id=id).update(
            sujestao=str(datetime.datetime.now()),
        )

        RegistroAtividades(
            cliente_id=Clientes.objects.get(id=id).id,
            registro='Sujestao Enviada alterada!',
            descricao=str(datetime.datetime.now()),
            assessor_responsavel=request.user.id
        ).save()

        response = 'Sujestao Enviada : <br>'+str(datetime.datetime.now())

    # SUJESTAO ALOCADA ---------------------------------------------------------
    if name == 'alocacao':
        ClientsOnbording.objects.filter(cliente_id=id).update(
            alocacao=str(datetime.datetime.now()),
        )

        RegistroAtividades(
            cliente_id=Clientes.objects.get(id=id).id,
            registro='Sujestao Alocada alterada!',
            descricao=str(datetime.datetime.now()),
            assessor_responsavel=request.user.id
        ).save()

        response = 'Sujestao Alocada : <br>'+str(datetime.datetime.now())

    return HttpResponse(response)

def update_observacao(request):
    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        onbording_obs=request.POST['obs'],
    )


    data = RegistroAtividades(
        cliente_id=Clientes.objects.get(id=request.POST['id']).id,
        registro='O Campo Observação foi alterado',
        descricao=request.POST['obs'],
        assessor_responsavel=request.user.id
    )
    data.save()

    response = 'ok'

    return HttpResponse(response)

def obrigado_questionario(request):

    return render(request, 'clients/obrigado.html')

def send_email_ondemand(request):
    data_atual = datetime.datetime.now()
    data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

    cliente = Clientes.objects.get(id=request.POST['id'])

    codigo = cliente.nickname
    token = hash(codigo)

    body = 'Responda o questionário no link abaixo <br> <a href="'+request.build_absolute_uri('/clientes/questionario/'+str(codigo)+'/'+str(token)+'/')+'">Responder questionário</a>'

    email = EmailMessage(
        'Questionário Onbording',
        # 'Renda Fixa',
        body,
        'Inove Investimentos |Seu Futuro Positivo <web@inoveinvestimentos.com.br>',
        # ['ccunhafinance@hotmail.com', ],
        ['ccunhafinance@gmail.com','bruno.martins@inoveinvestimentos.com.br'],
        # ['ccunhafinance@gmail.com','bruno.martins@inoveinvestimentos.com.br'],
        reply_to=['ondemand@inoveinvestimentos.com.br'],
        headers={'Message-ID': 'foo'},
    )

    email.content_subtype = "html"
    email.send()
    

    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        token=token,
        onbording_email=data_em_texto,
    )

    data = RegistroAtividades(
        cliente_id=Clientes.objects.get(id=request.POST['id']).id,
        registro='Email de questionamento enviado!',
        descricao='-',
        assessor_responsavel=request.user.id
    )
    data.save()

    return HttpResponse('ok')

def rotinaDone(request):
    id = request.POST['id']
    ClientsOnbording.objects.filter(cliente_id=id).update(
        is_done=True,
    )

    RegistroAtividades(
        cliente_id=Clientes.objects.get(id=id).id,
        registro='Rotina Onbording Concluida!',
        descricao=str(datetime.datetime.now()),
        assessor_responsavel=request.user.id
    ).save()

    return HttpResponse('ok')

def registroQuestionario(request):

    data = EnqueteOnbording(
        codigoDeCliente = request.POST['codigoDeCliente'],
        possuiParticipacaoSocietariaEmAlgumaEmpresa = request.POST['possuiParticipacaoSocietariaEmAlgumaEmpresa'],
        qualONomeDaEmpresa = request.POST['qualONomeDaEmpresa'],
        qualFaturamentoMedioAnualDaEmpresa = request.POST['qualFaturamentoMedioAnualDaEmpresa'],
        empresaPossuiSeguroDeVidaEmGrupo = request.POST['empresaPossuiSeguroDeVidaEmGrupo'],
        empresaPossuiPlanoDeSaudeParaFuncionarios = request.POST['empresaPossuiPlanoDeSaudeParaFuncionarios'],
        oSeuPlanoDeSaudeEAtravesDe = request.POST['oSeuPlanoDeSaudeEAtravesDe'],
        quantasVidasEstaoCobertasPeloSeuPlano = request.POST['quantasVidasEstaoCobertasPeloSeuPlano'],
        possuiAlgumaEstrategiaDeProtecaoPatrimonial = request.POST['possuiAlgumaEstrategiaDeProtecaoPatrimonial'],
        qualEstrategia = request.POST['qualEstrategia'],
        comQueFrequenciaRealizaOperacoesDeCambio = request.POST['comQueFrequenciaRealizaOperacoesDeCambio'],
        estrategiaProtecaoPatrimonialToGo = request.POST['estrategiaProtecaoPatrimonialToGo'],
        acompanhamentoPermanente = request.POST['acompanhamentoPermanente'],
        oportunidadesDeRendaFixa = request.POST['oportunidadesDeRendaFixa'],
        oportunidadesDeFundosDeInvestimentos = request.POST['oportunidadesDeFundosDeInvestimentos'],
        oportunidadesDeAcoes = request.POST['oportunidadesDeAcoes'],
        oportunidadesDeFundosImobiliarios = request.POST['oportunidadesDeFundosImobiliarios'],
        sujestao = request.POST['sujestao'],
    )

    data.save()

    return HttpResponse('Questionário salvo com sucesso!')

@transaction.atomic
def cleanGoogleNames(request):
    google = Clientes.objects.filter(cliente_dia=True, assessor=request.user.codigo).exclude(alldone=False)

    with transaction.atomic():
        for go in google:
            Clientes.objects.filter(id=int(go.id)).update(alldone=False)
  

    return redirect(reverse('clients:clients-onboarding'))

# PAGINA MEUS CLIENTES
def meusClientes(request):
   
    clientes = Clientes.objects.filter(assessor=request.user.codigo).exclude(status='Inativo')
    n_clientes = len(clientes)
    inativo = Clientes.objects.filter(status='Inativo',assessor=request.user.codigo)
    n_inativo = len(inativo)

    context = {
        'clientes': clientes,
        'n_clientes': n_clientes,
        'inativo': inativo,
        'n_inativo': n_inativo,
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

    return render(request, 'clients/meusclientes/list/base.html', context)

# PAGINA ONBOARDING
def onBording(request):
    onbording = ClientsOnbording.objects.filter(assessor=request.user.codigo).exclude(is_done=True).order_by('-id')
    n_onboarding = len(onbording)
    novos_clientes = Clientes.objects.filter(status='Novo',assessor=request.user.codigo).exclude(cliente_dia=True)
    inativo = Clientes.objects.filter(status='Inativo',assessor=request.user.codigo)
    google = Clientes.objects.filter(cliente_dia=True, assessor=request.user.codigo).exclude(alldone=False)
    n_contatos = len(Clientes.objects.filter(cliente_dia=True, assessor=request.user.codigo).exclude(alldone=False))
    n_inativo = len(inativo)
    n_novos_clientes = len(novos_clientes)
    i = Clientes.objects.filter(troca='interna',assessor=request.user.codigo).exclude(cliente_dia=True)
    j = Clientes.objects.filter(troca='externa',assessor=request.user.codigo).exclude(cliente_dia=True)
    troca_interna = len(i)
    troca_externa = len(j)

    context = {
        'n_onboarding': n_onboarding,
        'onbording': onbording,
        'inativo': inativo,
        'n_inativo': n_inativo,
        'novos_clientes': novos_clientes,
        'n_novos_clientes': n_novos_clientes,
        'n_troca_assessor': troca_interna,
        'n_troca_assessor_externa': troca_externa,
        'troca_assessor': i,
        'troca_assessor_externa': j,
        'contatos': google,
        'n_contatos': n_contatos,
        # Crumbs First Page Config
        'first_page_name': 'Clientes',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Onboarding',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': '',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Onboarding',
        'subtitle': '',
        'sticker': '',
        'page_description': 'Configuração Onboarding'
    }

    return render(request, 'clients/onbording/main/base.html', context)

# PAGINA ESPELHAMENTO
# ------------

    template_name = "clients/mirror_view.html"
    login_url = '/'

    def get_context_data( **kwargs):

        

        return context

# PAGINA ESPELHAMENTO
def espelhamento(request):
    clientes = Clientes.objects.all()
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

    return render(request, 'clients/espelhamento/main/base.html', context)

# PAGINA SALDO EM CONTA
def saldoConta(request):
    clientes = Clientes.objects.all()
    context = {
        'clientes': clientes,
        # Crumbs First Page Config
        'first_page_name': 'Clientes',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Saldo em Conta',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': '',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Saldo em Conta',
        'subtitle': '',
        'sticker': 'Novo',
        'page_description': ''
    }

    return render(request, 'clients/saldoemconta/main/base.html', context)

def rotina_emails(request, id):

    emails_cliente = NovoEmail.objects.filter(cliente_id=id)

    context = {
        'emails_cliente':emails_cliente,
        # Crumbs First Page Config
        'first_page_name': 'Clientes',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Rotina de emails',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': '',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Rotina',
        'subtitle': '',
        'sticker': 'Novo',
        'page_description': 'Listagem de clientes espelhados.'
    }

    return render(request, 'clients/rotina_view.html', context)

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

def get_cliente_data(request):
    clientes = Clientes.objects.all()


    code = request.POST['code']

    response = []
    for cliente in clientes:
        if cliente.assessor == code:

            response.append( '<tr>' \
                           '<td>'+ str(cliente.nickname) + '</td>'\
                           '<td>'+ str(cliente.nome) + '</td>'\
                           '<td>'+ '<a href="mailto:'+str(cliente.email)+'">'+str(cliente.email)+'</a>' + '</td>'\
                       '</th>')




    return HttpResponse(response)

