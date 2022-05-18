from django.http import HttpResponse
from django.shortcuts import render
from clients.models import Clientes
from users.models import *
from datetime import date, datetime
import pandas as pd
import json
import xlrd
from collections import OrderedDict
import glob
import os
from . models import *
from django.http import JsonResponse
from clients.models import RegistroAtividades


main_icon = 'fal fa-tasks'

def mainPageTarefas(request):
    hj = date.today()

    hora = datetime.now()

    if hora.hour >= 6 and hora.hour < 12:
        saldacao = 'Bom dia'
    elif hora.hour > 12 and hora.hour < 18:
        saldacao = 'Boa tarde'
    else:
        saldacao = 'Boa noite'

    clientes = Clientes.objects.filter(assessor=request.user.codigo, data_nascimento__month=hj.month).order_by('data_nascimento__day')

    list_of_files = glob.glob('data/files/vencimentoRF/*')
    xls = max(list_of_files, key=os.path.getctime)

    with open('data/files/vencimentoRF/vencimento.json') as json_file:
        vencimento = json.load(json_file)

    with open('data/files/vencimentoRF/saldoNegativo.json') as json_file:
        negativo = json.load(json_file)

    with open('data/files/vencimentoRF/saldoPositivo.json') as json_file:
        positivo = json.load(json_file)


    # print(len(vencimento))

   

    context = {
        'saldacao': saldacao,
        'clientes': clientes,
        'vencimento': vencimento,
        'negativos': negativo,
        'positivos': positivo,
        # Crumbs First Page Config
        'first_page_name': 'Tarefas',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Tarefas',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': '',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Tarefas',
        'subtitle': '',
        'sticker': '',
        'page_description': ''
    }

    return render(request, 'tarefas/main/base.html', context)

def regitroVencimentoRF(request):
    data = RegitroVencimentoRF(
        codigo_cliente = request.POST['codigo_cliente'],
        status =  request.POST['status']
    )

    data.save()

    data2 = RegistroAtividades(
        cliente_id=Clientes.objects.get(nickname=request.POST['codigo_cliente']).id,
        registro='Registro de Atividade Vencimento Renda Fixa',
        descricao=request.POST['status'],
        assessor_responsavel=request.user.id
    )
    data2.save()

    return HttpResponse('ok')

# convert para grana
def moedaConvert(my_value):
    a = '{:,.2f}'.format(float(my_value))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return c.replace('v','.')

def checkDvalue(value):
    if value < 0:
        return  "<span class='text-danger'>"+ 'R$ '+moedaConvert(value) +"</span>"
    elif value == 0:
        return  'R$ '+moedaConvert(value) 
    else:
        return  "<span class='text-info'>"+ 'R$ '+moedaConvert(value) +"</span>"

def clientesPositivos(request):
    hj = date.today()
    e = Clientes.objects.filter(assessor=request.user.codigo, d4__gt=0)
    positivos = []
    for cliente  in e:

        mens = ''
     
        
        if cliente.d0 < 0:
            mens += ' Saldo Negativo'

        
        if mens != '':
            alerta = ' <a data-original-title="Outras Tarefas" data-content="'+mens+'" href="javascript:void(0);" data-trigger="hover" data-placement="top" data-animation="true" class="btn btn-warning btn-sm btn-icon waves-effect waves-themed Mypopover"><i class="fal fa-exclamation-triangle"></i></a>'
        else:
            alerta = ''
     

        positivos.append(
            [
                cliente.data_nascimento,
                str(cliente.nickname), 
                str(cliente.nome), 
                checkDvalue(cliente.d0), 
                checkDvalue(cliente.d1), 
                checkDvalue(cliente.d2), 
                checkDvalue(cliente.d3), 
                checkDvalue(cliente.d4)
            ])

    return JsonResponse({"data": positivos})


def clientesNegativos(request):
    hj = date.today()
    e = Clientes.objects.filter(assessor=request.user.codigo, d0__lt=0)
    negativos = []
    for cliente  in e:

        mens = ''
        if hj.month == cliente.data_nascimento.month and hj.day == cliente.data_nascimento.day:
            mens += 'Aniversario '
    
       
        if cliente.d4 > 0:
            mens += ' Saldo Positivo'
       
        if mens != '':
            alerta = ' <a data-original-title="Outras Tarefas" data-content="'+mens+'" href="javascript:void(0);" data-trigger="hover" data-placement="top" data-animation="true" class="btn btn-warning btn-sm btn-icon waves-effect waves-themed Mypopover"><i class="fal fa-exclamation-triangle"></i></a>'
        else:
            alerta = ''

        negativos.append(
            [
                '', 
                str(cliente.nickname), 
                str(cliente.nome), 
                checkDvalue(cliente.d0), 
                checkDvalue(cliente.d1), 
                checkDvalue(cliente.d2), 
                checkDvalue(cliente.d3), 
                checkDvalue(cliente.d4)
            ])

    return JsonResponse({"data": negativos})

def getVencimentoRFtoJson(request):

    hora = datetime.now()

    if hora.hour >= 6 and hora.hour < 12:
        saldacao = 'Bom dia'
    elif hora.hour > 12 and hora.hour < 18:
        saldacao = 'Boa tarde'
    else:
        saldacao = 'Boa noite'


    list_of_files = glob.glob('data/files/vencimentoRF/*')
    xls = max(list_of_files, key=os.path.getctime)
  
    wb = xlrd.open_workbook(xls)
    sh = wb.sheet_by_name('Planilha1')

    data_list = []
					
    for rownum in range(1, sh.nrows):
        data = OrderedDict()
        row_values = sh.row_values(rownum)

        def formatBreak(item):
            result = ''
            for va in str(item).split(';'):
                result += (va+'<br>')
            return result

        def getzap(value):
            try:
                text =  Clientes.objects.get(nickname=value).telefone
                zap = text.replace('-','')
                zap = zap.replace(' ','')

                return '<a style="color:#25D366; text-decoration: none;font-size:10px" href="https://api.whatsapp.com/send?phone='+zap+'" target="_blank" rel="noopener">'+text+'</a>'

            except:
                return '--'

        def get_cliente_first_nome(value):
            try:
                return str(Clientes.objects.get(nickname=value).nome).split(' ')[0]

            except:
                return '-'

        def mens_contato1(value):
            val = '{0[0]}'.format(value)

            if val == '1':
                text = '%0DMeu nome é Lucas Thompson, sou assessor de investimentos aqui na Inove | XP e, em conjunto com o Bruno Martins, sou um dos responsáveis pela sua assessoria.%0D%0DAinda não tivemos a oportunidade de conversar, mas estava realizando o acompanhamento da sua conta e identifiquei que hoje tivemos o vencimento de um ativo de renda fixa.%0D%0D Você já sabe como alocar os recursos ou gostaria de uma assessoria.%0D%0D Segue abaixo o ativo e o valor bruto.%0D%0D Fico à disposição.'

                return text

            if val == '2':
                text = '%0DMeu nome é Lucas Thompson, sou assessor de investimentos aqui na Inove | XP e, em conjunto com o Bruno Martins, sou um dos responsáveis pela sua assessoria.%0D%0DAinda não tivemos a oportunidade de conversar, mas estava realizando o acompanhamento da sua conta e identifiquei que hoje tivemos o vencimento de ativos de renda fixa.%0D%0D Você já sabe como alocar os recursos ou gostaria de uma assessoria.%0D%0D Seguem abaixo os ativos e os valores brutos.%0D%0D Fico à disposição.'

                return text

            if val == '3':
                text = '%0DMeu nome é Lucas Thompson, sou assessor de investimentos aqui na Inove | XP e, em conjunto com o Bruno Martins, sou um dos responsáveis pela sua assessoria.%0D%0DAinda não tivemos a oportunidade de conversar, mas estava realizando o acompanhamento da sua conta e identifiquei que em breve teremos o vencimento de um ativo de renda fixa.%0D%0D Você já sabe como alocar os recursos ou gostaria de uma assessoria.%0D%0D Segue abaixo o ativo e o valor bruto.%0D%0D Fico à disposição.'

                return text

            if val == '4':
                text = '%0DMeu nome é Lucas Thompson, sou assessor de investimentos aqui na Inove | XP e, em conjunto com o Bruno Martins, sou um dos responsáveis pela sua assessoria.%0D%0DAinda não tivemos a oportunidade de conversar, mas estava realizando o acompanhamento da sua conta e identifiquei que em breve teremos o vencimento de ativos de renda fixa.%0D%0D Você já sabe como alocar os recursos ou gostaria de uma assessoria.%0D%0D Segu em abaixo os ativos e os valores brutos.%0D%0D Fico à disposição.'

                return text

            if val == '5':
                text = '%0DMeu nome é Lucas Thompson, sou assessor de investimentos aqui na Inove | XP e, em conjunto com o Bruno Martins, sou um dos responsáveis pela sua assessoria.%0D%0DAinda não tivemos a oportunidade de conversar, mas estava realizando o acompanhamento da sua conta e identifiquei que hoje tivemos um vencimento e que em breve teremos o vencimento de outros ativos de renda fixa.%0D%0D Você já sabe como alocar os recursos ou gostaria de uma assessoria.%0D%0D Seguem abaixo os ativos e os valores brutos.%0D%0D Fico à disposição.'

                return text
        
        # data['codeAssessor'] = row_values[9]
        data['codeCliente'] = row_values[0]
        data['nome'] = get_cliente_first_nome(row_values[0])
        data['ativo'] = formatBreak(row_values[1])
        data['vencimento'] = formatBreak(row_values[2])
        data['financeiro'] = formatBreak(row_values[3])
        data['Dt_Aplicacao'] = formatBreak(row_values[4])
        data['Qtd'] = formatBreak(row_values[5])
        data['PU_Atual'] = formatBreak(row_values[6])
        data['WhatsApp'] = getzap(row_values[0])
        data['nMensagem'] = '<a  style="color:#25D366; text-decoration: none" >a</a>'
        # data['mensagemFomat'] = row_values[8]
        if request.user.codigo == row_values[9]:
            data_list.append(data)

    return JsonResponse({"data": data_list})


   


  
   

