from django.shortcuts import render
import pandas as pd
import json
import xlrd
from collections import OrderedDict
import glob
import os


main_icon = 'fal fa-stars'

# PAGINA PRINCIPAL SEGURO
def pageDestaqueRendaFixa(request):

    list_of_files = glob.glob('data/files/destaqueRF/*')
    xls = max(list_of_files, key=os.path.getctime)
  
    wb = xlrd.open_workbook(xls)
    sh = wb.sheet_by_index(0)

    data_list = []
											
    for rownum in range(1, sh.nrows):
        data = OrderedDict()

        row_values = sh.row_values(rownum)
        data['Cliente'] = row_values[0]
        data['Assessor'] = row_values[1]
        data['AC'] = row_values[2]
        data['Ativo'] = row_values[3]
        data['Emissor'] = row_values[4]
        data['Indexador'] = row_values[5]
        data['Dt_Aplicacao'] = row_values[6]
        data['Vencimento'] = row_values[7]
        data['Carencia'] = row_values[8]
        data['Qtd'] = row_values[9]
        data['PU_Atual'] = row_values[10]
        data['Financeiro'] = row_values[11]
        data_list.append(data)
  

# Print out the result

    context = {
        # arquivo
        'destaques':data_list,
        # Crumbs First Page Config
        'first_page_name': 'Destaques',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Renda Fixa',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': '',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Destaques de Renda Fixa',
        'subtitle': '',
        'sticker': 'Novo',
        'page_description': ''
    }

    return render(request, 'destaques/rendafixa/base.html', context)

    # PAGINA PRINCIPAL SEGURO
def pageDestaqueSemana(request):

    context = {
        # Crumbs First Page Config
        'first_page_name': 'Destaques',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Semana',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': '',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Destaques da Semana',
        'subtitle': '',
        'sticker': 'Novo',
        'page_description': ''
    }

    return render(request, 'destaques/semana/base.html', context)
