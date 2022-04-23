from clients.models import Espelhamento, Clientes, ClientsOnbording
from yaml import SafeDumper, safe_dump, safe_dump_all, safe_load
from mail.models import EmailCategoria, Categoria
from users.models import UserProfile, CustomUser
from bs4 import BeautifulSoup
from datetime import datetime
from django import template
from numpy import safe_eval
from offers.models import *
from datetime import date
import pandas as pd
import locale
import json
import time
import os

register = template.Library()

# Get modalidades into Ofertas Ipo List View
@register.filter
def get_modalidade(value):
    modalidades = ModalidadeIpo.objects.filter(modalida=value)
    return modalidades

# Get series into Ofertas de Renda Fixa List View
@register.filter
def get_serie(value):
    series = SerieRf.objects.filter(serie=value)
    return series

# Formata moeda
@register.filter()
def moeda(value):
    if value == '' or value == None:
        return '-'
    else:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        valor = locale.currency(value, grouping=True, symbol=None)
        valor = 'R$ '+valor
        return valor

# Retorna diferença entre datas em modalidades
@register.filter(expects_localtime=True)
def days_since(value, arg=None):

    try:
        tzinfo = getattr(value, 'tzinfo', None)
        value = date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't a date object
        return value
    except ValueError:
        # Date arguments out of range
        return value
    today = datetime.now(tzinfo).date()
    delta = value - today

    return delta.days

# separa string em pontos determinados
@register.filter
def split(splitable, split_at):
    if len(split_at.split("||||")) == 2:
        return splitable.split(split_at.split("||||")[0], int(split_at.split("||||")[1]))
    return splitable.split(split_at)

# replaces

# Fii

# replace )
@register.filter
def replace_close_parent(value):
    first = value.replace(')','')
    return first

@register.filter
def find_negative(value):
    string = '-'
    teste = 'Cotação:'

    if value == '' :
        return 'nada'

    if not teste in value:
        return 'nada'

    if string in value:
        return True

# replace. por barra em data
@register.filter
def dot_to_bar(value):
    first = value.replace('.', '/')
    return first

# até por -
@register.filter
def ate_trace(value):
    first = value.replace('até', '<i class="fal fa-caret-right text-success"></i>')
    return first

@register.filter
def liquidacao(value):
    second = value.replace('Liquidação:', '<br><span class="text-danger">Liquidação: </span>')
    return second

@register.filter
def tiraporcentagem(value):
    
        a = value.replace('%', '')
        a = a.replace(',', '.')
        a = a.replace('', '')
        if a == '#N/D' or a == 'n/a' or a == '':
            return 'n/a'
        else:
            final = float(a)-100
            val = ('%.2f' %final)

            if final < 0:
                return "<span class='text-danger'> "+val.replace('.',',')+'%'+'</span>'
            else:
                return "<span class='text-success'> "+val.replace('.',',')+'%'+'</span>'
      
@register.filter
def replace_documentacao(value):
    if value == '':
        return "<span style='color:#fff'>>>>>>>></span>"
    else:
        soup = BeautifulSoup(value, 'lxml')
        text = soup.a
        if text == None:
            return soup.get_text()
        else:
       
            return text 

@register.filter
def getcliqueaqui(value):
   
        soup = BeautifulSoup(value, 'lxml')
        text = soup.a['href']

        # print(soup)
       
        return text

@register.filter
def checkdata(value):

    if value == 'n/a' or value == '':

        return '<span class="text-muted">'+value+"</span>"

    else:
        
        today = datetime.today().strftime('%d/%m/%Y')
        newdate1 = time.strptime(value, "%d/%m/%Y")
        newdate2 = time.strptime(today, "%d/%m/%Y")

        # print(newdate2)

        if newdate1 == newdate2:
            return '<span class="text-danger">'+value+"</span>"
        else:
            return '<span class="text-muted">'+value+"</span>"

@register.filter
def checkdatainicio(inicio, fim):

    if inicio == 'n/a' or inicio == '':

        return 'text-muted'

    else:

        today = datetime.today().strftime('%d/%m/%Y')
        start = time.strptime(inicio, "%d/%m/%Y")
        end = time.strptime(fim, "%d/%m/%Y")
        hoje = time.strptime(today, "%d/%m/%Y")

        if start <= hoje <= end:
            return 'text-info'
        else:
            return 'text-muted'

@register.filter
def getzap(value):
    return Clientes.objects.get(nickname=value).telefone

@register.filter
def getzapClean(value):
    zap =  Clientes.objects.get(nickname=value).telefone
    zap = zap.replace('-','')
    zap = zap.replace(' ','')
    return zap

@register.filter
def getjustnamefii(value):
    soup = BeautifulSoup(value, 'lxml')
    text = soup.get_text()
    return text

@register.filter
def takeoff11(value):
    first = value.replace('11', '')
    return first

@register.filter
def grab_fii_name(value):

    with open('data/ofertas/fii/fii_names.json') as json_file:
        fii_names = json.load(json_file)

    name_fii =''
    for name in fii_names:
        if value == name['Codigo']:
            name_fii = name['Nome']

    return name_fii

@register.filter
def user_image(value):
    image = UserProfile.objects.get(id=value)

    return image.image

@register.filter
def url_google_sheets(value):
    image = UserProfile.objects.get(id=value)

    return image.google_sheets

@register.filter
def user_check_pass(value):
    has = UserProfile.objects.get(id=value)

    return has.has_pass

# Ofertas

# IPO

# condicao para assunto do email
@register.filter
def assuntoemailipo(value):
    oferta = OfferRvIpo.objects.get(id=value)

    acoes_o = 'Ações Ordinárias da '
    acoes_p = 'Ações Preferenciais'
    acoes_o_p = 'Ações Ordinárias e Preferenciais'
    certificado = 'Certificados de Depósito de Ações Representativo de Ações Ordinárias Classe A'

    if oferta.tipe == 'acoes_o':
        if oferta.offer_pri == 'Sim' and oferta.offer_sec == 'Sim':
            subject = 'Reserva de Oferta Pública de Distribuição Primária e Secundária de ' + acoes_o +' da '+ oferta.company
        elif oferta.offer_pri == 'Não' and oferta.offer_sec == 'Sim':
            subject = 'Reserva de Oferta Pública de Distribuição Primária de ' + acoes_o +' da '+ oferta.company
        elif oferta.offer_pri == 'Sim' and oferta.offer_sec == 'Não':
            subject = 'Reserva de Oferta Pública de Distribuição Secundária de ' + acoes_o +' da '+ oferta.company

    elif oferta.tipe == 'acoes_p':

        if oferta.offer_pri == 'Sim' and oferta.offer_sec == 'Sim':
            subject = 'Reserva de Oferta Pública de Distribuição Primária e Secundária de ' + acoes_p +' da '+ oferta.company
        elif oferta.offer_pri == 'Não' and oferta.offer_sec == 'Sim':
            subject = 'Reserva de Oferta Pública de Distribuição Primária de ' + acoes_p +' da '+ oferta.company
        elif oferta.oferta_primaria == 'Sim' and oferta.offer_sec == 'Não':
            subject = 'Reserva de Oferta Pública de Distribuição Secundária de ' + acoes_p +' da '+ oferta.company

    elif oferta.tipe == 'acoes_o_p':
        if oferta.offer_pri == 'Sim' and oferta.offer_sec == 'Sim':
            subject = 'Reserva de Oferta Pública de Distribuição Primária e Secundária de ' + acoes_o_p +' da '+ oferta.company
        elif oferta.offer_pri == 'Não' and oferta.offer_sec == 'Sim':
            subject = 'Reserva de Oferta Pública de Distribuição Primária de ' + acoes_o_p +' da '+ oferta.company
        elif oferta.offer_pri == 'Sim' and oferta.offer_sec == 'Não':
            subject = 'Reserva de Oferta Pública de Distribuição Secundária de ' + acoes_o_p +' da '+ oferta.company

    else:
        subject = 'Reserva de Oferta Pública de Distribuição Secundária de ' + certificado +' da '+ oferta.company

    return subject

# filtro de Espelhamento
@register.filter
def get_assessor_ifos(value):

    assessor = CustomUser.objects.get(id=value)

    return assessor.codigo + ' - ' + assessor.first_name + ' ' + assessor.last_name

@register.filter
def get_assessor_fii_data(value):

    las_a = value.replace('A','')

    assessor = CustomUser.objects.get(codigo=las_a)

    return assessor.first_name + ' ' + assessor.last_name

@register.filter
def get_user_fii_data(value):


    assessor = CustomUser.objects.get(id=value)

    return assessor.codigo+ ' - ' +assessor.first_name + ' ' + assessor.last_name

@register.filter
def getCodeClient(value):
    return Clientes.objects.get(id=value).nickname

@register.filter
def format_aniversario(value):

    if str(value) == '00:00:00':
        return ''
    else:
        return str(value).split()[0]

@register.filter
def check_preenchido(value):
    t =  ClientsOnbording.objects.get(id=value).perfil_preenchido

    if t == None:
        return 'vazio'
    else:
        'ok'

@register.filter
def check_sugestao(value):
    t =  ClientsOnbording.objects.get(id=value).sujestao

    if t == None:
        return 'vazio'
    else:
        'ok'

@register.filter
def check_alocacao(value):
    t =  ClientsOnbording.objects.get(id=value).alocacao

    if t == None:
        return 'vazio'
    else:
        'ok'

@register.filter
def getNameClient(value):
    return Clientes.objects.get(id=value).nome

@register.filter
def get_cliente_nome(value):

    return Clientes.objects.get(nickname=str(value)).nome

@register.filter
def get_cliente_first_nome(value):
    return Clientes.objects.get(nickname=str(value)).nome

@register.filter
def calc_val_financeiro(preco, quant):

    a = preco.replace('R$ ', '')
    a = a.replace(',', '.')
    a = a.replace(' ', '')

    press = float(str(a))
    quantidade = int(quant)

    return press*quantidade

@register.filter
def get_assessor_ifos_by_code(value):

    assessor = CustomUser.objects.get(codigo=value)

    return assessor.codigo + ' - ' + assessor.first_name + ' ' + assessor.last_name

@register.filter
def get_assessor_ifos_by_id(value):

    if  value == None:
        return '-'
    else:

        assessor = CustomUser.objects.get(id=value)

        return assessor.codigo + ' - ' + assessor.first_name + ' ' + assessor.last_name

@register.filter
def check_espelho(value, arg):
    espelhos = Espelhamento.objects.filter(assessor_permited=value)

    new_value = ''
    for espelho in espelhos:
        if espelho.assessor_permited == value and espelho.assessor_id == arg:
            new_value = 'True'

    return new_value

@register.filter
def check_espelho_view(value, arg):
    id_assessor = CustomUser.objects.get(codigo=value)

    espelhos = Espelhamento.objects.filter(assessor_permited=id_assessor.id)

    new_value = ''
    for espelho in espelhos:
        if espelho.assessor_permited == id_assessor.id and espelho.assessor_id == arg:
            new_value = 'True'

    return new_value

@register.filter
def get_assessor_code(value):

    assessor = CustomUser.objects.get(id=value)

    return assessor.codigo

@register.filter
def get_assessor_id(value):
    take_A_off = value.replace('A','')

    id_assessor = CustomUser.objects.get(codigo=take_A_off)

    return str(id_assessor)

@register.filter
def str_val(value):
   return str(value)

@register.filter
def check_espelhamento_fii(id_assessor, arg):

    assessor_permited = int(arg)

    espelhos = Espelhamento.objects.filter(assessor_permited=assessor_permited)

    new_value = ''
    for espelho in espelhos:
        if espelho.assessor_permited ==  assessor_permited and espelho.assessor_id == int(id_assessor):
            new_value = 'True'

    # print(new_value)
    return new_value

@register.filter
def to_str(value):
    return str(value)

@register.filter
def cliente_code_replace(value):
    t = value.replace('A', '')
    las_a = str(t)
    return las_a

@register.filter
def get_assessor_code_nome_email(value):

    assessor = CustomUser.objects.get(id=value)

    return assessor.codigo + ' - ' + assessor.first_name + ' ' + assessor.last_name + ' - '+assessor.email

@register.filter
def isfile_here(value):

    if os.path.isfile('data/ofertas/fii/subscricao/' + str(value) + '.json'):
        return 'btn-success'
    else:
        return 'btn-danger'

def get_oferta(value):
    with open('data/ofertas/fii/ticker11_data.json') as json_file:
        ticker11 = json.load(json_file)

    oferta = []
    for ticker in ticker11:
        if ticker['Fundo'] == value:
            oferta = ticker
    return oferta

def calc_days(value):
        # return new_date
        try:
            tzinfo = getattr(value, 'tzinfo', None)
            value = date(value.year, value.month, value.day)
        except AttributeError:
            # Passed value wasn't a date object
            return value
        except ValueError:
            # Date arguments out of range
            return value
        today = datetime.now(tzinfo).date()
        delta = value - today

        return delta.days

@register.filter
def modalidade_adicional(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.get(id_oferta=d)

    if teste.modalidade_adicional is None:
        return ''
    else:
        return teste.modalidade_adicional

@register.filter
def nome_do_email(value):
    nome = EmailCategoria.objects.filter(id=value)

    return nome[0].nome

@register.filter
def nome_do_cat(value):
    nome = Categoria.objects.filter(id=value)
    return nome[0].nome

# FII EMAIL PAGE

@register.filter
def get_client_email(value):
    return Clientes.objects.get(nickname=value).email

@register.filter
def get_user_code_name(value):
    user = CustomUser.objects.get(id=value)

    return user.codigo+' - '+ user.first_name

@register.filter
def format_preco(value):
    return 'R$ '+ str(value).replace('.',',')

@register.filter
def val_fim_calc(val1, val2):
    result = val1*val2
    return 'R$ '+str(result).replace('.',',')

@register.filter
def check_email_sent(value, ticker):
    # print(ticker)
    try:
         a = RegisttoEmailFii.objects.filter(cliente=value, ticker=ticker).latest('id')
         print(a.data_envio)
         return a.data_envio
    except RegisttoEmailFii.DoesNotExist:
    # Passed value wasn't a date object
        return '-'
  


