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
    now = datetime.now()
    nome = now.strftime("%Y%m%d-%H%M%S")

    if request.method == 'POST':
        f=request.FILES['file']
        fs = FileSystemStorage(location='data/files/vencimentoRF')
        fs.save(str(nome)+'.xlsx', f)

        return HttpResponse('uploaded')
    else:
        return HttpResponse('error')

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

        