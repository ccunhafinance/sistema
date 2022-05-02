from django.shortcuts import render
from clients.models import Clientes
from users.models import *
from datetime import date, datetime


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
    saldo_positivo = Clientes.objects.filter(assessor=request.user.codigo, d4__gt=0).order_by('-d4')
    saldo_negativo = Clientes.objects.filter(assessor=request.user.codigo, d0__lt=0).order_by('d0')

    context = {
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