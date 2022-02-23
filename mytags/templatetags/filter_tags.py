import json
import os

from clients.models import Espelhamento
from offers.models import *
from django import template
import locale
from datetime import date
from datetime import datetime
from users.models import UserProfile, CustomUser

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
        valor = 'R$ %s' % +valor
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
def replace_documentacao(value):
    first = value.replace('<td>', '')
    second = first.replace('</td>', '')
    return second

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
def get_cliente_nome(value):

    with open('data/clientes/clientes.txt', encoding='latin1') as json_file:
        clientes = json.load(json_file)

    nome = ''
    for cliente in clientes:
        if cliente['CODIGO_XP_CLIENTE'] == int(value):
            nome = cliente['NOME_CLIENTE']

    # print(nome)

    return nome

@register.filter
def get_cliente_first_nome(value):
    with open('data/clientes/clientes.txt', encoding='latin1') as json_file:
        clientes = json.load(json_file)

    nome = ''
    for cliente in clientes:
        if cliente['CODIGO_XP_CLIENTE'] == int(value):
            nome = cliente['PRIMEIRO_NOME_CLIENTE']

    # print(nome)

    return nome


@register.filter
def calc_val_financeiro(preco, quant):

    a = preco.replace('R$ ','')
    b = a.replace(',','.')

    press = float(b)
    quantidade = int(quant)

    return press*quantidade


@register.filter
def get_assessor_ifos_by_code(value):

    assessor = CustomUser.objects.get(codigo=value)

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


# @register.filter
# def show_with_espelhamento(value, arg):
#     take_A_off = value.replace('A', '')
#
#     return new_value



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

# Identifica Grupos
@register.filter
def group(value):
    if value == "Não há" or value == "":
        validade = 'empty'
    else:
        validade = 'full'

    return validade

# Identifica Oferta
def get_oferta(value):
    with open('data/ofertas/fii/ticker11_data.json') as json_file:
        ticker11 = json.load(json_file)

    oferta = []
    for ticker in ticker11:
        if ticker['Fundo'] == value:
            oferta = ticker
    return oferta

# Calcula Dias
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

# Filater Data Inicial
def data_init(value):
    # separar valores enviados
    valores = value.split(' ')

    # organizando data inicial
    inicio = valores[0]

    x = inicio.split('.')
    now = datetime.now()

    if len(x) == 2:
        new_date = str(x[0]) + '/' + str(x[1].replace(' ', '')) + '/' + str(now.year)
    else:
        new_date = str(x[0]) + '/' + str(x[1].replace(' ', '')) + '/20' + str(x[2])

    data_inicial = new_date
    data_inicial = datetime.strptime(data_inicial, '%d/%m/%Y').date()

    dif_date = calc_days(data_inicial)

    return dif_date

# Filter Data Final
def data_fim(value):
    # separar valores enviados
    valores = value.split(' ')

    # organizando data final
    fim = valores[2]

    new_fim = fim.replace('Liquidação:', '')
    new_fim = new_fim.split('.')
    new_fim = str(new_fim[0]) + '/' + str(new_fim[1]) + '/20' + str(new_fim[2])

    data_final = datetime.strptime(new_fim, '%d/%m/%Y').date()
    dif_days = calc_days(data_final)

    return dif_days

# Filter Liquidação
def data_liquida(value):
    # separar valores enviados
    valores = value.split(' ')
    # print(valores)

    liquidacao = valores[3]

    if liquidacao == 'Pendente':
        return '-'
    else:
        liquidacao = liquidacao.split('.')
        liquidacao = str(liquidacao[0]) + '/' + str(liquidacao[1]) + '/20' + str(liquidacao[2])

        liquidacao = datetime.strptime(liquidacao, '%d/%m/%Y').date()

        dif_days = calc_days(liquidacao)

        return dif_days

# Grupo (1) - Período Público
@register.filter(expects_localtime=True)
def group_one(value):

    oferta = get_oferta(value)

    data_inicio = data_init(oferta['PeríodoPúblico'])
    data_final = data_fim(oferta['PeríodoPúblico'])
    liquid = data_liquida(oferta['PeríodoPúblico'])

    if data_inicio > 0:
        return '<span class="text-info"><span class="text-info">Aguardando Período Pública</span></span>'
    if data_inicio == 0:
        return '<span class="text-success">1* Dia Período Pública</span>'
    if data_inicio < 0 and data_final >= 0:
        return '<span class="text-success">Período Oferta Pública</span>'
    if data_final == 0:
        return '<span style="color: #e67e22">Último Dia Período Pública</span>'
    if liquid > 0:
        return '<span class="text-info"><span class="text-info">Aguardando Liquidação Período Pública</span></span>'
    if liquid == 0:
        return '<span class="text-danger">Liquidação Período Pública</span>'
    if liquid < 0:
        return '<span class="text-info"><span class="text-info">Aguardando Encerramento</span></span>'

# Grupo (2) - Período Público, Período de Preferência
@register.filter(expects_localtime=True)
def group_two(value):

    oferta = get_oferta(value)

    # Periodo Público
    data_pub_inicio = data_init(oferta['PeríodoPúblico'])
    data_pub_final = data_fim(oferta['PeríodoPúblico'])
    data_pub_liquid = data_liquida(oferta['PeríodoPúblico'])

    # Período de Preferência
    data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    if data_pref_inicio > 0:
        return '<span class="text-info">Aguardando Período de Preferência</span>'
    if data_pref_inicio == 0:
        return '<span class="text-success">1* Dia Período de Preferência</span>'
    if data_pref_inicio < 0 and data_pref_final > 0:
        return '<span class="text-success">Período de Preferência</span>'
    if data_pref_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Preferência</span>'
    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'

    if data_pub_inicio > 0:
        return '<span class="text-info">Aguardando Período Pública</span>'
    if data_pub_inicio == 0:
        return '<span class="text-success">1* Dia Período Pública</span>'
    if data_pub_inicio < 0 and data_pub_final >= 0:
        return '<span class="text-success">Período Oferta Pública</span>'
    if data_pub_final == 0:
        return '<span style="color: #e67e22">Último Dia Período Pública</span>'
    if data_pub_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período Pública</span>'
    if data_pub_liquid == 0:
        return '<span class="text-danger">Liquidação Período Pública</span>'
    if data_pub_liquid < 0:
        return '<span class="text-info">Aguardando Encerramento</span>'

# Grupo (3) - Período de Preferência, Período de Sobras, Período Público
@register.filter(expects_localtime=True)
def group_three(value):

    oferta = get_oferta(value)

    # Período de Preferência
    data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    # Período de Sobra
    data_sobra_inicio = data_init(oferta['PeríododeSobras'])
    data_sobra_final = data_fim(oferta['PeríododeSobras'])
    data_sobra_liquid = data_liquida(oferta['PeríododeSobras'])

    # Periodo Público
    data_pub_inicio = data_init(oferta['PeríodoPúblico'])
    data_pub_final = data_fim(oferta['PeríodoPúblico'])
    data_pub_liquid = data_liquida(oferta['PeríodoPúblico'])

    if data_pref_inicio > 0:
        return '<span class="text-info">Aguardando Período de Preferência</span>'
    if data_pref_inicio == 0:
        return '<span class="text-success">1* Dia Período de Preferência</span>'
    if data_pref_inicio < 0 and data_pref_final > 0:
        return '<span class="text-success">Período de Preferência</span>'
    if data_pref_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Preferência</span>'
    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'

    if data_sobra_inicio > 0:
        return '<span class="text-info">Aguardando Período de Sobras</span>'
    if data_sobra_inicio == 0:
        return '<span class="text-success">1* Dia Período de Sobras</span>'
    if data_sobra_inicio < 0 and data_sobra_final >= 0:
        return '<span class="text-success">Período de Sobras</span>'
    if data_sobra_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Sobras</span>'
    if data_sobra_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Sobras</span>'
    if data_sobra_liquid == 0:
        return '<span class="text-danger">Liquidação de Sobras</span>'

    if data_pub_inicio > 0:
        return '<span class="text-info">Aguardando Período Pública</span>'
    if data_pub_inicio == 0:
        return '<span class="text-success">1* Dia Período Pública</span>'
    if data_pub_inicio < 0 and data_pub_final >= 0:
        return '<span class="text-success">Período Pública</span>'
    if data_pub_final == 0:
        return '<span style="color: #e67e22">Último Dia Período Pública</span>'
    if data_pub_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período Pública</span>'
    if data_pub_liquid == 0:
        return '<span class="text-danger">Liquidação Período Pública</span>'
    if data_pub_liquid < 0:
        return '<span class="text-info">Aguardando Encerramento</span>'

# Grupo (4) - Período de Negociação, Períodode Preferência, Período de Sobras, Período Público
@register.filter(expects_localtime=True)
def group_four(value):

    oferta = get_oferta(value)

    # Periodo de Negociação
    data_negoci_inicio = data_init(oferta['PeríododeNegociação'])
    data_negoci_final = data_fim(oferta['PeríododeNegociação'])

    # Período de Preferência
    data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    # Período de Sobra
    data_sobra_inicio = data_init(oferta['PeríododeSobras'])
    data_sobra_final = data_fim(oferta['PeríododeSobras'])
    data_sobra_liquid = data_liquida(oferta['PeríododeSobras'])

    # Periodo Público
    data_pub_inicio = data_init(oferta['PeríodoPúblico'])
    data_pub_final = data_fim(oferta['PeríodoPúblico'])
    data_pub_liquid = data_liquida(oferta['PeríodoPúblico'])

    if data_negoci_inicio > 0:
        return '<span class="text-info">Aguardando Período de Negociação e Preferência</span>'
    if data_negoci_inicio == 0:
        return '<span class="text-success">1* Dia Período de Negociação e Preferência</span>'
    if data_negoci_inicio < 0 and data_negoci_final > 0:
        return '<span class="text-success">Período de Negociação e Preferência</span>'
    if data_negoci_final == 0 and data_pref_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Negociação e Preferência</span>'
    if data_negoci_final > 0 and data_pref_final < 0:
        return '<span style="color: #e67e22">Último Dia Período de Negociação e Período de Preferência Ativo</span>'
    if data_negoci_final < 0 and data_pref_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Preferência</span>'

    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'

    if data_sobra_inicio > 0:
        return '<span class="text-info">Aguardando Período de Sobras</span>'
    if data_sobra_inicio == 0:
        return '<span class="text-success">1* Dia Período de Sobras</span>'
    if data_sobra_inicio < 0 and data_sobra_final >= 0:
        return '<span class="text-success">Período de Sobras</span>'
    if data_sobra_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Sobras</span>'
    if data_sobra_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Sobras</span>'
    if data_sobra_liquid == 0:
        return '<span class="text-danger">Liquidação de Sobras</span>'

    if data_pub_inicio > 0:
        return '<span class="text-info">Aguardando Período Pública</span>'
    if data_pub_inicio == 0:
        return '<span class="text-success">1* Dia Período Pública</span>'
    if data_pub_inicio < 0 and data_pub_final >= 0:
        return '<span class="text-success">Período Oferta Pública</span>'
    if data_pub_final == 0:
        return '<span style="color: #e67e22">Último Dia Período Pública</span>'
    if data_pub_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período Pública</span>'
    if data_pub_liquid == 0:
        return '<span class="text-danger">Liquidação Período Pública</span>'
    if data_pub_liquid < 0:
        return '<span class="text-info">Aguardando Encerramento</span>'

# Grupo (5) - Períodode Preferência
@register.filter(expects_localtime=True)
def group_five(value):

    oferta = get_oferta(value)

    data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    if data_pref_inicio > 0:
        return '<span class="text-info">Aguardando Período de Preferência</span>'
    if data_pref_inicio == 0:
        return '<span class="text-success">1* Dia Período de Preferência</span>'
    if data_pref_inicio < 0 and data_pref_final > 0:
        return '<span class="text-success">Período de Preferência</span>'
    if data_pref_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Preferência</span>'
    if data_pref_liquid == '-':
        return '<span class="text-danger">Pendente/span>'
    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'
    if data_pref_liquid < 0:
        return '<span class="text-info">Aguardando Encerramento</span>'

# Grupo (6) - Períodode Preferência, Período de Sobras
@register.filter(expects_localtime=True)
def group_six(value):

    oferta = get_oferta(value)

    # Período de Preferencia
    data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    # Período de Sobra
    data_sobra_inicio = data_init(oferta['PeríododeSobras'])
    data_sobra_final = data_fim(oferta['PeríododeSobras'])
    data_sobra_liquid = data_liquida(oferta['PeríododeSobras'])

    if data_pref_inicio > 0:
        return '<span class="text-info">Aguardando Período de Preferência</span>'
    if data_pref_inicio == 0:
        return '<span class="text-success">1* Dia Período de Preferência</span>'
    if data_pref_inicio < 0 and data_pref_final > 0:
        return '<span class="text-success">Período de Preferência</span>'
    if data_pref_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Preferência</span>'
    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'

    if data_sobra_inicio > 0:
        return '<span class="text-info">Aguardando Período de Sobras</span>'
    if data_sobra_inicio == 0:
        return '<span class="text-success">1* Dia Período de Sobras</span>'
    if data_sobra_inicio < 0 and data_sobra_final > 0:
        return '<span class="text-success">Período de Sobras</span>'
    if data_sobra_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Sobras</span>'
    if data_sobra_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Sobras</span>'
    if data_sobra_liquid == 0:
        return '<span class="text-danger">Liquidação de Sobras</span>'
    if data_sobra_liquid < 0:
        return '<span class="text-info">Aguardando Encerramento</span>'

# Grupo (7) - Período de Negociação, Períodode Preferência, Período de Sobras
@register.filter(expects_localtime=True)
def group_seven(value):

    oferta = get_oferta(value)

    # Periodo de Negociação
    data_negoci_inicio = data_init(oferta['PeríododeNegociação'])
    data_negoci_final = data_fim(oferta['PeríododeNegociação'])

    # Período de Preferência
    # data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    # Período de Sobra
    data_sobra_inicio = data_init(oferta['PeríododeSobras'])
    data_sobra_final = data_fim(oferta['PeríododeSobras'])
    data_sobra_liquid = data_liquida(oferta['PeríododeSobras'])


    if data_negoci_inicio > 0:
        return '<span class="text-info">Aguardando Período de Negociação e Preferência</span>'
    if data_negoci_inicio == 0:
        return '<span class="text-success">1* Dia Período de Negociação e Preferência</span>'
    if data_negoci_inicio < 0 and data_negoci_final > 0:
        return '<span class="text-success">Período de Negociação e Preferência</span>'
    if data_negoci_final == 0 and data_pref_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Negociação e Preferência</span>'
    if data_negoci_final > 0 and data_pref_final < 0:
        return '<span style="color: #e67e22">Último Dia Período de Negociação e Período de Preferência Ativo</span>'
    if data_negoci_final < 0 and data_pref_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Preferência</span>'

    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'

    if data_sobra_inicio > 0:
        return '<span class="text-info">Aguardando Período de Sobras</span>'
    if data_sobra_inicio == 0:
        return '<span class="text-success">1* Dia Período de Sobras</span>'
    if data_sobra_inicio < 0 and data_sobra_final > 0:
        return '<span class="text-success">Período de Sobras</span>'
    if data_sobra_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Sobras</span>'
    if data_sobra_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Sobras</span>'
    if data_sobra_liquid == 0:
        return '<span class="text-danger">Liquidação de Sobras</span>'
    if data_sobra_liquid < 0:
            return '<span class="text-info">Aguardando Encerramento</span>'

# Grupo (8) - Período de Negociação, Períodode Preferência
@register.filter(expects_localtime=True)
def group_eight(value):

    oferta = get_oferta(value)

    # Periodo de Negociação
    data_negoci_inicio = data_init(oferta['PeríododeNegociação'])
    data_negoci_final = data_fim(oferta['PeríododeNegociação'])

    # Período de Preferência
    # data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    if data_negoci_inicio > 0:
        return '<span class="text-info">Aguardando Período de Negociação e Preferência</span>'
    if data_negoci_inicio == 0:
        return '<span class="text-success">1* Dia Período de Negociação e Preferência</span>'
    if data_negoci_inicio < 0 and data_negoci_final > 0:
        return '<span class="text-success">Período de Negociação e Preferência</sapn>'
    if data_negoci_final == 0 and data_pref_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Negociação e Preferência</span>'
    if data_negoci_final > 0 and data_pref_final < 0:
        return '<span style="color: #e67e22">Último Dia Período de Negociação e Período de Preferência Ativo</span>'
    if data_negoci_final < 0 and data_pref_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Preferência</span>'

    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'
    if data_pref_liquid < 0:
        return '<span class="text-info">Aguardando Encerramento</span>'

# Grupo (9) - Período de Negociação, Períodode Preferência, Período Público
@register.filter(expects_localtime=True)
def group_nine(value):
    oferta = get_oferta(value)

    # Periodo de Negociação
    data_negoci_inicio = data_init(oferta['PeríododeNegociação'])
    data_negoci_final = data_fim(oferta['PeríododeNegociação'])

    # Período de Preferência
    # data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    # Periodo Público
    data_pub_inicio = data_init(oferta['PeríodoPúblico'])
    data_pub_final = data_fim(oferta['PeríodoPúblico'])
    data_pub_liquid = data_liquida(oferta['PeríodoPúblico'])

    if data_negoci_inicio > 0:
        return '<span class="text-info">Aguardando Período de Negociação e Preferência</span>'
    if data_negoci_inicio == 0:
        return '<span class="text-success">1* Dia Período de Negociação e Preferência</span>'
    if data_negoci_inicio < 0 and data_negoci_final > 0:
        return '<span class="text-success">Período de Negociação e Preferência</span>'
    if data_negoci_final == 0 and data_pref_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Negociação e Preferência</span>'
    if data_negoci_final > 0 and data_pref_final < 0:
        return '<span style="color: #e67e22">Último Dia Período de Negociação e Período de Preferência Ativo</span>'
    if data_negoci_final < 0 and data_pref_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Preferência</span>'

    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'

    if data_pub_inicio > 0:
        return '<span class="text-info">Aguardando Período Pública</span>'
    if data_pub_inicio == 0:
        return '<span class="text-success">1* Dia Período Pública</span>'
    if data_pub_inicio < 0 and data_pub_final >= 0:
        return '<span class="text-success">Período Oferta Pública</span>'
    if data_pub_final == 0:
        return '<span style="color: #e67e22">Último Dia Período Pública</span>'
    if data_pub_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período Pública</span>'
    if data_pub_liquid == 0:
        return '<span class="text-danger">Liquidação Período Pública</span>'
    if data_pub_liquid < 0:
        return '<span class="text-info">Aguardando Encerramento</span>'


# MENSAGENS ----------------------------------

# MENSAGENS (1) - Período Público
@register.filter(expects_localtime=True)
def mensagens_one(value):

    oferta = get_oferta(value)

    data_inicio = data_init(oferta['PeríodoPúblico'])
    data_final = data_fim(oferta['PeríodoPúblico'])
    liquid = data_liquida(oferta['PeríodoPúblico'])

    if data_inicio > 0:
        return '<span class="text-info"><span class="text-info">Aguardando Período Pública</span></span>'
    if data_inicio == 0:
        return 'Msg 1'
    if data_inicio < 0 and data_final >= 0:
        return 'Msg 2'
    if data_final == 0:
        return 'Msg 3'
    if liquid > 0:
        return '<span class="text-info"><span class="text-info">Aguardando Liquidação Período Pública</span></span>'
    if liquid == 0:
        return '<span class="text-danger">Liquidação Período Pública</span>'
    if liquid < 0:
        return '<span class="text-info"><span class="text-info">Aguardando Encerramento</span></span>'

# MENSAGENS (2) - Período Público, Período de Preferência
@register.filter(expects_localtime=True)
def mensagens_two(value):

    oferta = get_oferta(value)

    # Periodo Público
    data_pub_inicio = data_init(oferta['PeríodoPúblico'])
    data_pub_final = data_fim(oferta['PeríodoPúblico'])
    data_pub_liquid = data_liquida(oferta['PeríodoPúblico'])

    # Período de Preferência
    data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    if data_pref_inicio > 0:
        return '<span class="text-info">Aguardando Período de Preferência</span>'
    if data_pref_inicio == 0:
        return '<span class="text-success">1* Dia Período de Preferência</span>'
    if data_pref_inicio < 0 and data_pref_final > 0:
        return 'Msg 4'
    if data_pref_final == 0:
        return 'Msg 5'
    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'

    if data_pub_inicio > 0:
        return '<span class="text-info">Aguardando Período Pública</span>'
    if data_pub_inicio == 0:
        return 'Msg 1'
    if data_pub_inicio < 0 and data_pub_final >= 0:
        return 'Msg 2'
    if data_pub_final == 0:
        return 'Msg 3'
    if data_pub_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período Pública</span>'
    if data_pub_liquid == 0:
        return '<span class="text-danger">Liquidação Período Pública</span>'
    if data_pub_liquid < 0:
        return '<span class="text-info">Aguardando Encerramento</span>'

# MENSAGENS (3) - Período de Preferência, Período de Sobras, Período Público
@register.filter(expects_localtime=True)
def mensagens_three(value):

    oferta = get_oferta(value)

    # Período de Preferência
    data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    # Período de Sobra
    data_sobra_inicio = data_init(oferta['PeríododeSobras'])
    data_sobra_final = data_fim(oferta['PeríododeSobras'])
    data_sobra_liquid = data_liquida(oferta['PeríododeSobras'])

    # Periodo Público
    data_pub_inicio = data_init(oferta['PeríodoPúblico'])
    data_pub_final = data_fim(oferta['PeríodoPúblico'])
    data_pub_liquid = data_liquida(oferta['PeríodoPúblico'])

    if data_pref_inicio > 0:
        return '<span class="text-info">Aguardando Período de Preferência</span>'
    if data_pref_inicio == 0:
        return '<span class="text-success">1* Dia Período de Preferência</span>'
    if data_pref_inicio < 0 and data_pref_final > 0:
        return 'Msg 4'
    if data_pref_final == 0:
        return 'Msg 5'
    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'

    if data_sobra_inicio > 0:
        return '<span class="text-info">Aguardando Período de Sobras</span>'
    if data_sobra_inicio == 0:
        return '<span class="text-success">1* Dia Período de Sobras</span>'
    if data_sobra_inicio < 0 and data_sobra_final >= 0:
        return '<span class="text-success">Período de Sobras</span>'
    if data_sobra_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Sobras</span>'
    if data_sobra_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Sobras</span>'
    if data_sobra_liquid == 0:
        return '<span class="text-danger">Liquidação de Sobras</span>'

    if data_pub_inicio > 0:
        return '<span class="text-info">Aguardando Período Pública</span>'
    if data_pub_inicio == 0:
        return 'Msg 1'
    if data_pub_inicio < 0 and data_pub_final >= 0:
        return 'Msg 2'
    if data_pub_final == 0:
        return '<span style="color: #e67e22">Último Dia Período Pública</span>'
    if data_pub_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período Pública</span>'
    if data_pub_liquid == 0:
        return '<span class="text-danger">Liquidação Período Pública</span>'
    if data_pub_liquid < 0:
        return '<span class="text-info">Aguardando Encerramento</span>'

# MENSAGENS (4) - Período de Negociação, Períodode Preferência, Período de Sobras, Período Público
@register.filter(expects_localtime=True)
def mensagens_four(value):

    oferta = get_oferta(value)

    # Periodo de Negociação
    data_negoci_inicio = data_init(oferta['PeríododeNegociação'])
    data_negoci_final = data_fim(oferta['PeríododeNegociação'])

    # Período de Preferência
    data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    # Período de Sobra
    data_sobra_inicio = data_init(oferta['PeríododeSobras'])
    data_sobra_final = data_fim(oferta['PeríododeSobras'])
    data_sobra_liquid = data_liquida(oferta['PeríododeSobras'])

    # Periodo Público
    data_pub_inicio = data_init(oferta['PeríodoPúblico'])
    data_pub_final = data_fim(oferta['PeríodoPúblico'])
    data_pub_liquid = data_liquida(oferta['PeríodoPúblico'])

    if data_negoci_inicio > 0:
        return '<span class="text-info">Aguardando Período de Negociação e Preferência</span>'
    if data_negoci_inicio == 0:
        return '<span class="text-success">1* Dia Período de Negociação e Preferência</span>'
    if data_negoci_inicio < 0 and data_negoci_final > 0:
        return 'Msg 7'
    if data_negoci_final == 0 and data_pref_final == 0:
        return 'Msg 8'
    if data_negoci_final > 0 and data_pref_final < 0:
        return '<span style="color: #e67e22">Último Dia Período de Negociação e Período de Preferência Ativo</span>'
    if data_negoci_final < 0 and data_pref_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Preferência</span>'

    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'

    if data_sobra_inicio > 0:
        return '<span class="text-info">Aguardando Período de Sobras</span>'
    if data_sobra_inicio == 0:
        return '<span class="text-success">1* Dia Período de Sobras</span>'
    if data_sobra_inicio < 0 and data_sobra_final >= 0:
        return '<span class="text-success">Período de Sobras</span>'
    if data_sobra_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Sobras</span>'
    if data_sobra_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Sobras</span>'
    if data_sobra_liquid == 0:
        return '<span class="text-danger">Liquidação de Sobras</span>'

    if data_pub_inicio > 0:
        return '<span class="text-info">Aguardando Período Pública</span>'
    if data_pub_inicio == 0:
        return 'Msg 1'
    if data_pub_inicio < 0 and data_pub_final >= 0:
        return 'Msg 2'
    if data_pub_final == 0:
        return 'Msg 3'
    if data_pub_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período Pública</span>'
    if data_pub_liquid == 0:
        return '<span class="text-danger">Liquidação Período Pública</span>'
    if data_pub_liquid < 0:
        return '<span class="text-info">Aguardando Encerramento</span>'

# MENSAGENS (5) - Períodode Preferência
@register.filter(expects_localtime=True)
def mensagens_five(value):

    oferta = get_oferta(value)

    data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    if data_pref_inicio > 0:
        return '<span class="text-info">Aguardando Período de Preferência</span>'
    if data_pref_inicio == 0:
        return '<span class="text-success">1* Dia Período de Preferência</span>'
    if data_pref_inicio < 0 and data_pref_final > 0:
        return 'Msg 4'
    if data_pref_final == 0:
        return 'Msg 5'
    if data_pref_liquid == '-':
        return '<span class="text-danger">Pendente/span>'
    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'
    if data_pref_liquid < 0:
        return '<span class="text-info">Aguardando Encerramento</span>'

# MENSAGENS (6) - Períodode Preferência, Período de Sobras
@register.filter(expects_localtime=True)
def mensagens_six(value):

    oferta = get_oferta(value)

    # Período de Preferencia
    data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    # Período de Sobra
    data_sobra_inicio = data_init(oferta['PeríododeSobras'])
    data_sobra_final = data_fim(oferta['PeríododeSobras'])
    data_sobra_liquid = data_liquida(oferta['PeríododeSobras'])

    if data_pref_inicio > 0:
        return '<span class="text-info">Aguardando Período de Preferência</span>'
    if data_pref_inicio == 0:
        return '<span class="text-success">1* Dia Período de Preferência</span>'
    if data_pref_inicio < 0 and data_pref_final > 0:
        return 'Msg 4'
    if data_pref_final == 0:
        return 'Msg 5'
    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'

    if data_sobra_inicio > 0:
        return '<span class="text-info">Aguardando Período de Sobras</span>'
    if data_sobra_inicio == 0:
        return '<span class="text-success">1* Dia Período de Sobras</span>'
    if data_sobra_inicio < 0 and data_sobra_final > 0:
        return '<span class="text-success">Período de Sobras</span>'
    if data_sobra_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Sobras</span>'
    if data_sobra_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Sobras</span>'
    if data_sobra_liquid == 0:
        return '<span class="text-danger">Liquidação de Sobras</span>'
    if data_sobra_liquid < 0:
        return '<span class="text-info">Aguardando Encerramento</span>'

# MENSAGENS (7) - Período de Negociação, Períodode Preferência, Período de Sobras
@register.filter(expects_localtime=True)
def mensagens_seven(value):

    oferta = get_oferta(value)

    # Periodo de Negociação
    data_negoci_inicio = data_init(oferta['PeríododeNegociação'])
    data_negoci_final = data_fim(oferta['PeríododeNegociação'])

    # Período de Preferência
    # data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    # Período de Sobra
    data_sobra_inicio = data_init(oferta['PeríododeSobras'])
    data_sobra_final = data_fim(oferta['PeríododeSobras'])
    data_sobra_liquid = data_liquida(oferta['PeríododeSobras'])


    if data_negoci_inicio > 0:
        return '<span class="text-info">Aguardando Período de Negociação e Preferência</span>'
    if data_negoci_inicio == 0:
        return '<span class="text-success">1* Dia Período de Negociação e Preferência</span>'
    if data_negoci_inicio < 0 and data_negoci_final > 0:
        return 'Msg 7'
    if data_negoci_final == 0 and data_pref_final == 0:
        return 'Msg 8'
    if data_negoci_final > 0 and data_pref_final < 0:
        return '<span style="color: #e67e22">Último Dia Período de Negociação e Período de Preferência Ativo</span>'
    if data_negoci_final < 0 and data_pref_final == 0:
        return 'Msg 8'

    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'

    if data_sobra_inicio > 0:
        return '<span class="text-info">Aguardando Período de Sobras</span>'
    if data_sobra_inicio == 0:
        return '<span class="text-success">1* Dia Período de Sobras</span>'
    if data_sobra_inicio < 0 and data_sobra_final > 0:
        return '<span class="text-success">Período de Sobras</span>'
    if data_sobra_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Sobras</span>'
    if data_sobra_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Sobras</span>'
    if data_sobra_liquid == 0:
        return '<span class="text-danger">Liquidação de Sobras</span>'
    if data_sobra_liquid < 0:
            return '<span class="text-info">Aguardando Encerramento</span>'

# MENSAGENS (8) - Período de Negociação, Períodode Preferência
@register.filter(expects_localtime=True)
def mensagens_eight(value):

    oferta = get_oferta(value)

    # Periodo de Negociação
    data_negoci_inicio = data_init(oferta['PeríododeNegociação'])
    data_negoci_final = data_fim(oferta['PeríododeNegociação'])

    # Período de Preferência
    # data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    if data_negoci_inicio > 0:
        return '<span class="text-info">Aguardando Período de Negociação e Preferência</span>'
    if data_negoci_inicio == 0:
        return '<span class="text-success">1* Dia Período de Negociação e Preferência</span>'
    if data_negoci_inicio < 0 and data_negoci_final > 0:
        return 'Msg 7'
    if data_negoci_final == 0 and data_pref_final == 0:
        return 'Msg 8'
    if data_negoci_final > 0 and data_pref_final < 0:
        return '<span style="color: #e67e22">Último Dia Período de Negociação e Período de Preferência Ativo</span>'
    if data_negoci_final < 0 and data_pref_final == 0:
        return 'Msg 8'

    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'
    if data_pref_liquid < 0:
        return '<span class="text-info">Aguardando Encerramento</span>'

# MENSAGENS (9) - Período de Negociação, Períodode Preferência, Período Público
@register.filter(expects_localtime=True)
def mensagens_nine(value):
    oferta = get_oferta(value)

    # Periodo de Negociação
    data_negoci_inicio = data_init(oferta['PeríododeNegociação'])
    data_negoci_final = data_fim(oferta['PeríododeNegociação'])

    # Período de Preferência
    # data_pref_inicio = data_init(oferta['PeríododePreferência'])
    data_pref_final = data_fim(oferta['PeríododePreferência'])
    data_pref_liquid = data_liquida(oferta['PeríododePreferência'])

    # Periodo Público
    data_pub_inicio = data_init(oferta['PeríodoPúblico'])
    data_pub_final = data_fim(oferta['PeríodoPúblico'])
    data_pub_liquid = data_liquida(oferta['PeríodoPúblico'])

    if data_negoci_inicio > 0:
        return '<span class="text-info">Aguardando Período de Negociação e Preferência</span>'
    if data_negoci_inicio == 0:
        return '<span class="text-success">1* Dia Período de Negociação e Preferência</span>'
    if data_negoci_inicio < 0 and data_negoci_final > 0:
        return 'Msg 7'
    if data_negoci_final == 0 and data_pref_final == 0:
        return 'Msg 8'
    if data_negoci_final > 0 and data_pref_final < 0:
        return '<span style="color: #e67e22">Último Dia Período de Negociação e Período de Preferência Ativo</span>'
    if data_negoci_final < 0 and data_pref_final == 0:
        return '<span style="color: #e67e22">Último Dia Período de Preferência</span>'

    if data_pref_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período de Preferência</span>'
    if data_pref_liquid == 0:
        return '<span class="text-danger">Liquidação de Preferência</span>'

    if data_pub_inicio > 0:
        return '<span class="text-info">Aguardando Período Pública</span>'
    if data_pub_inicio == 0:
        return 'Msg 1'
    if data_pub_inicio < 0 and data_pub_final >= 0:
        return 'Msg 2'
    if data_pub_final == 0:
        return '<span style="color: #e67e22">Último Dia Período Pública</span>'
    if data_pub_liquid > 0:
        return '<span class="text-info">Aguardando Liquidação Período Pública</span>'
    if data_pub_liquid == 0:
        return '<span class="text-danger">Liquidação Período Pública</span>'
    if data_pub_liquid < 0:
        return '<span class="text-info">Aguardando Encerramento</span>'

# MENSAGENS ----------------------------------

# identificandocores dob email
@register.filter
def put_colors(value):


    a = "Aguardando"
    b = "Último Dia"
    c = 'Liquidação'


    if a in value:
        color = '<span class="bola-info" style="position:absolute;"></span>'

    elif b in value:
        color = '<span class="bola-orange" style="position:absolute;"></span>'

    elif c in value:
        color = '<span class="bola-danger" style="position:absolute;"></span>'

    else:
        color = '<span class="bola-success" style="position:absolute;"></span>'


    return color

@register.filter
def allowed_email(value):
   a = 'Aguardando'
   b = 'Liquidação'

   if a in value:
       mail = 'close'

   elif b in value:
       mail = 'close'
   else:
       mail = 'open'

   return mail

# @register.filter(expects_localtime=True)
# def days_since(value, arg=None):days_since
#     try:
#         tzinfo = getattr(value, 'tzinfo', None)
#         value = date(value.year, value.month, value.day)
#     except AttributeError:
#         # Passed value wasn't a date object
#         return value
#     except ValueError:
#         # Date arguments out of range
#         return value
#     today = datetime.now(tzinfo).date()
#     delta = value - today
#     if abs(delta.days) == 1:
#         day_str = ("day")
#     else:
#         day_str = ("days")
#
#     if delta.days < 1:
#         fa_str = ("ago")
#     else:
#         fa_str = ("from now")
#
#     return "%s %s %s" % (abs(delta.days), day_str, fa_str)

# fii edits

@register.filter
def check_if_has_aedits(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.filter(id_oferta=d)


    if len(teste) == 1:
       return 'ok'
    else:
        return 'nok'

@register.filter
def check_if_has_aedits_ok(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.get(id_oferta=d)


    return int(teste.id)

@register.filter
def check_if_has_aedits_database(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.get(id_oferta=d)

    if teste.data_base is None:
        return ''
    else:
        return teste.data_base

@register.filter
def check_if_has_aedits_pnegocia_inicio(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.get(id_oferta=d)

    if teste.inicio_periodo_de_negociacao is None:
        return ''
    else:
        return teste.inicio_periodo_de_negociacao

@register.filter
def check_if_has_aedits_pnegocia_fim(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.get(id_oferta=d)

    if teste.fim_periodo_de_negociacao is None:
        return ''
    else:
        return teste.fim_periodo_de_negociacao


@register.filter
def inicio_periodo_preferencia(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.get(id_oferta=d)

    if teste.inicio_periodo_preferencia is None:
        return ''
    else:
        return teste.inicio_periodo_preferencia

@register.filter
def fim_periodo_preferencia(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.get(id_oferta=d)

    if teste.fim_periodo_preferencia is None:
        return ''
    else:
        return teste.fim_periodo_preferencia

@register.filter
def liquidacao_periodo_preferencia(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.get(id_oferta=d)

    if teste.liquidacao_periodo_preferencia is None:
        return ''
    else:
        return teste.liquidacao_periodo_preferencia






@register.filter
def inicio_periodo_sobra(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.get(id_oferta=d)

    if teste.inicio_periodo_sobra is None:
        return ''
    else:
        return teste.inicio_periodo_sobra

@register.filter
def fim_periodo_sobra(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.get(id_oferta=d)

    if teste.fim_periodo_sobra is None:
        return ''
    else:
        return teste.fim_periodo_sobra

@register.filter
def liquidacao_periodo_sobra(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.get(id_oferta=d)

    if teste.liquidacao_periodo_sobra is None:
        return ''
    else:
        return teste.liquidacao_periodo_sobra



@register.filter
def inicio_periodo_publico(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.get(id_oferta=d)

    if teste.inicio_periodo_publico is None:
        return ''
    else:
        return teste.inicio_periodo_publico

@register.filter
def fim_periodo_publico(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.get(id_oferta=d)

    if teste.fim_periodo_publico is None:
        return ''
    else:
        return teste.fim_periodo_publico

@register.filter
def liquidacao_periodo_publico(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.get(id_oferta=d)

    if teste.liquidacao_periodo_publico is None:
        return ''
    else:
        return teste.liquidacao_periodo_publico


@register.filter
def modalidade_adicional(value, arg):

    d = value+''+arg

    teste = FiiEdit.objects.get(id_oferta=d)

    if teste.modalidade_adicional is None:
        return ''
    else:
        return teste.modalidade_adicional


