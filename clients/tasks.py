from celery import shared_task
from django.core.mail import send_mail
from time import sleep
from core.celery import app
import datetime
from clients.models import *
from datetime import date
import json
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.urls import reverse
from clients.models import Espelhamento, NovoEmail, RegistroAtividades
from .models import Clientes
from mail.models import *
from .resources import ClientesResources
from django.contrib import messages
from tablib import Dataset
from datetime import date
import datetime
import time
from django.db import transaction
import pandas as pd

@shared_task
def sleepy(duration):
    sleep(duration)
    return None

   

@shared_task
def upload_novos_clientes(primeiro):

      primeiro_file = pd.read_json(primeiro)
      data_atual =  datetime.datetime.now()
      data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

      # print (len(clientes))

      # print(imported_data)

      clients_first_upload = []
      for data in primeiro_file:

            replacement = data[7]
            s = data[1].split()
            s[0] = replacement
            nome_atualiazado = ' '.join(s)

            value = Clientes(
                    nickname='cu',
                    nome=str(nome_atualiazado).title(),
                    assessor=data[2],
                    sexo=data[3],
                    email=data[4],
                    telefone=data[5],
                    data_nascimento=data[6],
                    data_registro=data_em_texto
                )
            clients_first_upload.append(value)
      Clientes.objects.bulk_create(clients_first_upload)
                

@shared_task
def segundo_upload(a, b):
    clientes = Clientes.objects.all()
    data_atual =  datetime.datetime.now()
    data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')
    base_exel_external = pd.read_json(b).to_numpy()
    base_exel_all = pd.read_json(a).to_numpy()

    # print(base_exel_external)
    # print(base_exel_all)

    # ----------- check clientes inativos
    t = len(base_exel_all)
    a = 0

    db_clientes =[]
    for cliente in clientes:
        db_clientes.append(str(cliente.nickname))

    xsl_sheet = []
    for cliente in base_exel_all:
        if a < t:
            xsl_sheet.append(str(base_exel_all[a][0]))
        a += 1

    def Diff(li1, li2):
        return list(set(li1) - set(li2))

    inativos = Diff(db_clientes, xsl_sheet)

    if len(inativos) > 0:
        with transaction.atomic():
            for x in inativos:
                Clientes.objects.filter(nickname=x).update(
                    status='Inativo',
                    data_registro=data_em_texto
                )

    # # Check se tem troca de assessores internos
    def func():
        for x in base_exel_all:
            yield x

    troca_interna = func()
    for item in troca_interna:
        for cliente in clientes:
            if str(cliente.nickname) == str(item[0]) and str(cliente.assessor) != str(item[2]):
                Clientes.objects.filter(nickname=cliente.nickname).update(
                    nome=str(item[1]).title(),
                    assessor=item[2],
                    antigo_assessor=cliente.assessor,
                    d0=item[3],
                    d1=item[4],
                    d2=item[5],
                    d3=item[6],
                    d4=item[7],
                    troca='interna',
                    data_registro=data_em_texto
                )
            
    # Check se cliente que ja existe tem algum campo alterado

    alteracao_dados = func()
    with transaction.atomic():
        for item in alteracao_dados:
            for cliente in clientes:
                if str(cliente.nickname) == str(item[0]):
                    Clientes.objects.filter(nickname=cliente.nickname).update(
                    nome=str(item[1]).title(),
                    d0=item[3],
                    d1=item[4],
                    d2=item[5],
                    d3=item[6],
                    d4=item[7],
                    data_registro=data_em_texto
                )

    # Novos Clientes

    v = len(base_exel_all)
    b = 0

    ex_clientes = []
    for cliente in clientes:
        ex_clientes.append([str(cliente.nickname), cliente.nome, str(cliente.assessor), cliente.d0, cliente.d1, cliente.d2, cliente.d3, cliente.d4])

    tab_clientes = []
    for cliente in base_exel_all:
        if b < v:
            tab_clientes.append([str(base_exel_all[b][0]), base_exel_all[b][1], base_exel_all[b][2], base_exel_all[b][3], base_exel_all[b][4], base_exel_all[b][5], base_exel_all[b][6], base_exel_all[b][7]])
        b += 1

    def igual(x, y):
        if x[0] == y[0]:
            return True
        else:
            return False
    
    novos_clientes = []
    for x in tab_clientes:
        tem = False
        for y in ex_clientes:
            if igual(x,y):
                tem =True
                break
        if not tem:
            novos_clientes.append(x)

    # print(len(novos_clientes))

    if len(novos_clientes) > 0:
        new_insert = []
        for cliente in novos_clientes:
            value = Clientes(
                nickname=cliente[0],
                nome=str(cliente[1]).title(),
                assessor=cliente[2],
                d0=cliente[3],
                d1=cliente[4],
                d2=cliente[5],
                d3=cliente[6],
                d4=cliente[7],
                status='Novo',
                data_registro=data_em_texto
            )
            new_insert.append(value)
        Clientes.objects.bulk_create(new_insert)
    
    tran_externa = []
    for data in base_exel_external:
        if data[3] != '-' and data[7] == 'CONCLUÍDO':
            tran_externa.append([str(data[1])])

    
    with transaction.atomic():
        for t_x in tran_externa:
            print(Clientes.objects.filter(nickname=str(t_x[0])))
            Clientes.objects.filter(nickname=t_x[0]).update(
                    troca='externa',
                    status='Novo',
                    data_registro=data_em_texto
                )

      

      


    #   t = len(df1)
    #   a = 0
    #   primeiro =[]
    #   segundo = []

    #   for cliente in clientes:

    #       primeiro.append(str(cliente.nickname))

    #       if a < t:
    #           segundo.append(str(df1.to_numpy()[a][0]))

    #       a += 1

    #   def Diff(li1, li2):
    #       return list(set(li1) - set(li2))

    #   # Inativa Cliente
    #   # print(Diff(primeiro, segundo))

    #   inativos = Diff(primeiro, segundo)
    #   for x in inativos:
    #         Clientes.objects.filter(nickname=x).update(
    #             status='Inativo',
    #             data_registro=data_em_texto
    #         )
    #   insert_cleintes = []
      
    #   for data in df1.to_numpy():
    #         # print(data)
    #         if len(Clientes.objects.filter(nickname=data[0])) == 1:

    #             if str(Clientes.objects.filter(nickname=data[0])[0].assessor) != str(data[2]):
    #                 Clientes.objects.filter(nickname=data[0]).update(
    #                     nome=str(data[1]).title(),
    #                     assessor=data[2],
    #                     antigo_assessor=Clientes.objects.filter(nickname=data[0])[0].assessor,
    #                     d0=data[3],
    #                     d1=data[4],
    #                     d2=data[5],
    #                     d3=data[6],
    #                     d4=data[7],
    #                     troca='interna',
    #                     data_registro=data_em_texto
    #                 )
    #             else:

    #                 Clientes.objects.filter(nickname=data[0]).update(
    #                     nome=str(data[1]).title(),
    #                     d0=data[3],
    #                     d1=data[4],
    #                     d2=data[5],
    #                     d3=data[6],
    #                     d4=data[7],
    #                     data_registro=data_em_texto
    #                 )
    #         else:

    #             value = Clientes(
    #                 nickname=data[0],
    #                 nome=str(data[1]).title(),
    #                 assessor=data[2],
    #                 d0=data[3],
    #                 d1=data[4],
    #                 d2=data[5],
    #                 d3=data[6],
    #                 d4=data[7],
    #                 status='Novo',
    #                 data_registro=data_em_texto
    #             )
    #             insert_cleintes.append(value)
    #   Clientes.objects.bulk_create(insert_cleintes)
            
    #   ncliente =[]
    #   for data in df2.to_numpy():
    #       # print(data)

    #       if len(Clientes.objects.filter(nickname=data[1])) == 1 and  len(data[3]) > 1 and data[7] == 'CONCLUÍDO':
    #           Clientes.objects.filter(nickname=data[1]).update(
    #                   # nome=str(data[1]).title(),
    #                   assessor=data[3].split('-')[0].replace(" ", ""),
    #                   # antigo_assessor=Clientes.objects.filter(nickname=data[0])[0].assessor,
    #                   # d0=data[3],
    #                   # d1=data[4],
    #                   # d2=data[5],
    #                   # d3=data[6],
    #                   # d4=data[7],
    #                   troca='externa',
    #                   status='Novo',
    #                   data_registro=data[6]
    #               )
    #       elif len(data[3]) > 1 and data[7] == 'CONCLUÍDO':
    #           value = Clientes(
    #               nickname=data[1],
    #               # nome=str(data[1]).title(),
    #               assessor=data[3].split('-')[0].replace(" ", ""),
    #               # d0=data[3],
    #               # d1=data[4],
    #               # d2=data[5],
    #               # d3=data[6],
    #               # d4=data[7],
    #               troca='externa',
    #               status='Novo',
    #               data_registro=data[6]
    #           )
    #           ncliente.append(value)
    #   Clientes.objects.bulk_create(ncliente)   

