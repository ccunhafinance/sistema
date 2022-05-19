from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.views import generic
import xlrd
from collections import OrderedDict
import json
from django.contrib.auth.decorators import login_required
import datetime
from datetime import date, datetime
import os, glob
from pathlib import Path
from clients.models import Clientes



main_icon = 'fal fa-cogs'

# PAGINA PRINCIPAL SEGURO
def pageUploadArquivos(request):

    
    context = {
        # files path
        'vencimentorf': os.listdir('data/files/vencimentoRF')[::-1],
        'destaquerf': os.listdir('data/files/destaqueRF')[::-1],
        'custodiafii': os.listdir('data/files/custodiaFII')[::-1],
        'custodiarv': os.listdir('data/files/custodiaRV')[::-1],
        # Crumbs First Page Config
        'first_page_name': 'Configurações',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Upload de Arquivos',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': '',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Upload de Arquivos',
        'subtitle': '',
        'sticker': 'Novo',
        'page_description': ''
    }

    return render(request, 'configuracoes/uploadarquivos/base.html', context)

def uploadVencimentoRF(request):
    # now = datetime.now()
    # nome = now.strftime("%Y%m%d-%H%M%S")
    hj = date.today()
    niver = Clientes.objects.filter(assessor=request.user.codigo,data_nascimento__month=hj.month, data_nascimento__day=hj.day).exclude(data_nascimento__isnull=True)

    if request.method == 'POST':
        f=request.FILES['file']
        fs = FileSystemStorage(location='data/files/vencimentoRF')
        fs.save(str('vencimento')+'.xlsx', f)
        # fs.save('data/files/vencimentoRF/vencimento.xlsx', f)

        # list_of_files = glob.glob('data/files/vencimentoRF/*')
        # xls = max(list_of_files, key=os.path.getctime)

        # wb = xlrd.open_workbook(xls)
        wb = xlrd.open_workbook('data/files/vencimentoRF/vencimento.xlsx')
        sh = wb.sheet_by_name('Planilha1')

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

        def telefone(value):
            try:
                text =  Clientes.objects.get(nickname=value).telefone
                zap = text.replace('-','')
                zap = zap.replace(' ','')

                return zap

            except:
                return '--'

        def get_cliente_first_nome(value):
            try:
                return str(Clientes.objects.get(nickname=value).nome).split(' ')[0]

            except:
                return '-'

        def primeiro_contato(value):
            val = str(value)

            if val == '1':
                text = '%0DMeu nome é Lucas Thompson, sou assessor de investimentos aqui na Inove | XP e, em conjunto com o Bruno Martins, sou um dos responsáveis pela sua assessoria.%0D%0DAinda não tivemos a oportunidade de conversar, mas estava realizando o acompanhamento da sua conta e identifiquei que hoje tivemos o vencimento de um ativo de renda fixa.%0D%0DVocê já sabe como alocar os recursos ou gostaria de uma assessoria?%0D%0DSegue abaixo o ativo e o valor bruto.%0D%0DFico à disposição.'

                return text

            if val == '2':
                text = '%0DMeu nome é Lucas Thompson, sou assessor de investimentos aqui na Inove | XP e, em conjunto com o Bruno Martins, sou um dos responsáveis pela sua assessoria.%0D%0DAinda não tivemos a oportunidade de conversar, mas estava realizando o acompanhamento da sua conta e identifiquei que hoje tivemos o vencimento de ativos de renda fixa.%0D%0DVocê já sabe como alocar os recursos ou gostaria de uma assessoria?%0D%0DSeguem abaixo os ativos e os valores brutos.%0D%0DFico à disposição.'

                return text

            if val == '3':
                text = '%0DMeu nome é Lucas Thompson, sou assessor de investimentos aqui na Inove | XP e, em conjunto com o Bruno Martins, sou um dos responsáveis pela sua assessoria.%0D%0DAinda não tivemos a oportunidade de conversar, mas estava realizando o acompanhamento da sua conta e identifiquei que em breve teremos o vencimento de um ativo de renda fixa.%0D%0DVocê já sabe como alocar os recursos ou gostaria de uma assessoria?%0D%0D Segue abaixo o ativo e o valor bruto.%0D%0DFico à disposição.'

                return text

            if val == '4':
                text = '%0DMeu nome é Lucas Thompson, sou assessor de investimentos aqui na Inove | XP e, em conjunto com o Bruno Martins, sou um dos responsáveis pela sua assessoria.%0D%0DAinda não tivemos a oportunidade de conversar, mas estava realizando o acompanhamento da sua conta e identifiquei que em breve teremos o vencimento de ativos de renda fixa.%0D%0DVocê já sabe como alocar os recursos ou gostaria de uma assessoria?%0D%0D Segu em abaixo os ativos e os valores brutos.%0D%0DFico à disposição.'

                return text

            if val == '5':
                text = '%0DMeu nome é Lucas Thompson, sou assessor de investimentos aqui na Inove | XP e, em conjunto com o Bruno Martins, sou um dos responsáveis pela sua assessoria.%0D%0DAinda não tivemos a oportunidade de conversar, mas estava realizando o acompanhamento da sua conta e identifiquei que hoje tivemos um vencimento e que em breve teremos o vencimento de outros ativos de renda fixa.%0D%0DVocê já sabe como alocar os recursos ou gostaria de uma assessoria?%0D%0DSeguem abaixo os ativos e os valores brutos.%0D%0DFico à disposição.'

                return text
        

        data_list = []

        allcodesVencimento = []
					
    for rownum in range(1, sh.nrows):
        data = OrderedDict()
        row_values = sh.row_values(rownum)

       
        def contato_padrao(value):
            val = str(value)

            if val == '1':
                text = '%0DIdentifiquei que hoje tivemos o vencimento de um ativo de renda fixa na sua conta.%0D%0DVocê já sabe como alocar os recursos ou gostaria de uma assessoria?%0D%0DSegue abaixo o ativo e o valor bruto.%0D%0DFico à disposição.'

                return text
            
            if val == '2':
                text = '%0DIdentifiquei que hoje tivemos o vencimento de ativos de renda fixa na sua conta.%0D%0DVocê já sabe como alocar os recursos ou gostaria de uma assessoria?%0D%0DSeguem abaixo os ativos e os valores brutos.%0D%0DFico à disposição.'

                return text

            if val == '3':
                text = '%0DIdentifiquei que em breve teremos o vencimento de um ativo de renda fixa na sua conta.%0D%0DVocê já sabe como alocar os recursos ou gostaria de uma assessoria?%0D%0DSegue abaixo o ativo e o valor bruto.%0D%0DFico à disposição.'

                return text

            if val == '4':
                text = '%0DIdentifiquei que em breve teremos o vencimento de ativos de renda fixa na sua conta.%0D%0DVocê já sabe como alocar os recursos ou gostaria de uma assessoria?%0D%0DSeguem abaixo os ativos e os valores brutos.%0D%0DFico à disposição.'

                return text

            if val == '5':
                text = '%0DIdentifiquei que hoje tivemos um vencimento e que em breve teremos o vencimento de outros ativos de renda fixa na sua conta.%0D%0DVocê já sabe como alocar os recursos ou gostaria de uma assessoria?%0D%0DSeguem abaixo os ativos e os valores brutos.%0D%0DFico à disposição.'

                return text
        
        def checkTarefas(value):
            saldo_positivo = Clientes.objects.filter(nickname=value, d4__gt=0).order_by('-d4')
            saldo_negativo = Clientes.objects.filter(nickname=value, d0__lt=0).order_by('d0')

            result = ''

            for ania in niver:
                if ania.nickname == value:
                    result += 'Aniversario '

            if len(saldo_negativo) == 1:
                result += 'Saldo Negativo '

            if len(saldo_positivo) == 1:
                result += ' Saldo Positivo'

            if result == '':
                resp = ''
            else:
                resp = result

            ans = '<a onclick="getalertAll('"'"+value+"'"')" data-original-title="Outras Tarefas" data-content="'+resp+'" href="javascript:void(0);" data-trigger="hover" data-placement="top" data-animation="true" class="btn btn-warning btn-sm btn-icon waves-effect waves-themed Mypopover"><i class="fal fa-exclamation-triangle"></i></a>'

            if resp == '':
                final = ''
            else:
                final = ans

            return final

        if row_values[0] != '':
            data['id'] = Clientes.objects.get(nickname=int(row_values[0])).id
            data['alerta'] = checkTarefas(row_values[0])
            data['assessor'] = row_values[9]
            data['codeCliente'] = row_values[0]
            allcodesVencimento.append(row_values[0])
            data['nome'] = get_cliente_first_nome(row_values[0])
            data['ativo'] = formatBreak(row_values[1])
            data['vencimento'] = formatBreak(row_values[2])
            data['financeiro'] = formatBreak(row_values[3])
            data['Dt_Aplicacao'] = formatBreak(row_values[4])
            data['Qtd'] = formatBreak(row_values[5])
            data['PU_Atual'] = formatBreak(row_values[6])
            data['WhatsApp'] = getzap(row_values[0])
            data['telefone'] = telefone(row_values[0])
            data['primeiroContato'] = primeiro_contato(row_values[7])
            data['contatoPadrao'] = contato_padrao(row_values[7]) 
            data['todosAtivos'] = row_values[8]
            if request.user.codigo == row_values[9]:
                data_list.append(data)

    with open('data/files/vencimentoRF/vencimento.json', "w", encoding="utf-8") as writeJsonfile:
            json.dump(data_list, writeJsonfile, indent=4, default=str)


    fs.delete('vencimento.xlsx')


    # clientes NEGATIVO ----------------------------------------------------------------------------------------------------------------

    
    sNegativo = Clientes.objects.filter(assessor=request.user.codigo, d0__lt=0)

    negativos = []
    for cliente  in sNegativo:
        data = OrderedDict()

        mens = ''

        if cliente.nickname in allcodesVencimento:
                mens += 'Vencimento RF '

        for ania in niver:
            if ania.nickname == cliente.nickname:
                mens += 'Aniversario '

        if mens != '':
            alerta = ' <a onclick="getalertAll('"'"+cliente.nickname+"'"')" data-original-title="Outras Tarefas" data-content="'+mens+'" href="javascript:void(0);" data-trigger="hover" data-placement="top" data-animation="true" class="btn btn-warning btn-sm btn-icon waves-effect waves-themed Mypopover"><i class="fal fa-exclamation-triangle"></i></onclick=>'
        else:
            alerta = ''
        data['id'] = cliente.id
        data['alerta'] = alerta
        data['codigo'] = cliente.nickname
        data['WhatsApp'] = getzap(cliente.nickname)
        data['d0'] = cliente.d0
        data['d1'] = cliente.d1
        data['d2'] = cliente.d2
        data['d3'] = cliente.d3
        data['d4'] = cliente.d4
        if request.user.codigo == cliente.assessor:
            negativos.append(data)

    # print(negativos)

    with open('data/files/vencimentoRF/saldoNegativo.json', "w", encoding="utf-8") as writeJsonfile:
        json.dump(negativos, writeJsonfile, indent=4, default=str)

    # clientes POSITIVO ----------------------------------------------------------------------------------------------------------------
    
    sPositivo = Clientes.objects.filter(assessor=request.user.codigo, d4__gt=0)

    positivos = []
    for cliente  in sPositivo:
        data = OrderedDict()
        
        mens = ''
    
        if cliente.nickname in allcodesVencimento:
                mens += 'Vencimento RF '

        for ania in niver:
            if ania.nickname == cliente.nickname:
                mens += 'Aniversario '
       
        if mens != '':
            alerta = ' <a onclick="getalertAll('"'"+cliente.nickname+"'"')" data-original-title="Outras Tarefas" data-content="'+mens+'" href="javascript:void(0);" data-trigger="hover" data-placement="top" data-animation="true" class="btn btn-warning btn-sm btn-icon waves-effect waves-themed Mypopover"><i class="fal fa-exclamation-triangle"></i></a>'
        else:
            alerta = ''

        data['id'] = cliente.id
        data['alerta'] = alerta
        data['codigo'] = cliente.nickname
        data['WhatsApp'] = getzap(cliente.nickname)
        data['d0'] = cliente.d0
        data['d1'] = cliente.d1
        data['d2'] = cliente.d2
        data['d3'] = cliente.d3
        data['d4'] = cliente.d4
        if request.user.codigo == cliente.assessor:
            positivos.append(data)

    # print(positivos)

    with open('data/files/vencimentoRF/saldoPositivo.json', "w", encoding="utf-8") as writeJsonfile:
        json.dump(positivos, writeJsonfile, indent=4, default=str)

    return HttpResponse('uploaded')


    

def uploadDestaqueRF(request):
    now = datetime.now()
    nome = now.strftime("%Y%m%d-%H%M%S")

    if request.method == 'POST':
        f=request.FILES['file']
        fs = FileSystemStorage(location='data/files/destaqueRF')
        fs.save(str(nome)+'.xlsx', f)

        return HttpResponse('uploaded')
    else:
        return HttpResponse('error')

def uploadCustodiaFII(request):
    now = datetime.now()
    nome = now.strftime("%Y%m%d-%H%M%S")

    if request.method == 'POST':
        f=request.FILES['file']
        fs = FileSystemStorage(location='data/files/custodiaFII')
        fs.save(str(nome)+'.xlsx', f)

        return HttpResponse('uploaded')
    else:
        return HttpResponse('error')

def uploadCustodiaRV(request):
    now = datetime.now()
    nome = now.strftime("%Y%m%d-%H%M%S")

    if request.method == 'POST':
        f=request.FILES['file']
        fs = FileSystemStorage(location='data/files/custodiaRV')
        fs.save(str(nome)+'.xlsx', f)

        return HttpResponse('uploaded')
    else:
        return HttpResponse('error')

        