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


main_icon = 'fal fa-tasks'

def mainPageTarefas(request):

    list_of_files = glob.glob('data/files/vencimentoRF/*')
    xls = max(list_of_files, key=os.path.getctime)
  
    wb = xlrd.open_workbook(xls)
    sh = wb.sheet_by_name('Planilha1')

    data_list = []
											
    for rownum in range(1, sh.nrows):
        data = OrderedDict()

        row_values = sh.row_values(rownum)
        data['Cliente'] = str(row_values[0]).replace('.0','')
        data['Ativo'] = row_values[1]
        data['Vencimento'] = row_values[2]
        data['Financeiro'] = row_values[3]
        data['Dt_Aplicacao'] = row_values[4]
        data['Qtd'] = str(row_values[5]).replace('.0','')
        data['PU_Atual'] = row_values[6] 
        data_list.append(data)

    hj = date.today()

    hora = datetime.now()

    if hora.hour >= 6 and hora.hour < 12:
        saldacao = 'Bom dia'
    elif hora.hour > 12 and hora.hour < 18:
        saldacao = 'Boa tarde'
    else:
        saldacao = 'Boa noite'

    clientes = Clientes.objects.filter(assessor=request.user.codigo, data_nascimento__month=hj.month).order_by('data_nascimento__day')
    saldo_positivo = Clientes.objects.filter(assessor=request.user.codigo, d4__gt=0).order_by('-d4')
    saldo_negativo = Clientes.objects.filter(assessor=request.user.codigo, d0__lt=0).order_by('d0')

    context = {
        'vencimento': data_list,
        'saldacao': saldacao,
        'clientes': clientes,
        'saldo_positivo': saldo_positivo,
        'saldo_negativo': saldo_negativo,
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
        'sticker': 'Novo',
        'page_description': ''
    }

    return render(request, 'tarefas/main/base.html', context)