from celery import shared_task
from django.core.mail import send_mail
from time import sleep
from core.celery import app
import datetime
from clients.models import *
from datetime import date

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

import pandas as pd

@shared_task
def sleepy(duration):
    sleep(duration)
    return None

   

@shared_task
def upload_novos_clientes(new_cliente):

  try:
      clientes_resource = ClientesResources()
      dataset = Dataset()
      clientes = Clientes.objects.all()

      data_atual =  datetime.datetime.now()
      data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

      # print (len(clientes))

      # print(imported_data)

      if len(clientes)==0:

          imported_data = dataset.load(new_cliente.read(), format='xlsx')

          for data in imported_data:

              # print(data)

              try:
                  listing = Clientes.objects.get(nickname=data[1])

              except Clientes.DoesNotExist:
                  value = Clientes(
                      nickname=data[1],
                      nome=str(data[2]).title(),
                      sexo=data[3],
                      email=data[4],
                      telefone=data[5],
                      assessor=data[6],
                      data_nascimento=data[7],
                      data_registro=data_em_texto
                  )
                  value.save()

      else:
          # imported_data = pd.read_excel(new_cliente, sheet_name='tab2')
          # pd.set_option('display.max_rows', None)
          xls = pd.ExcelFile(new_cliente)
          df1 = pd.read_excel(xls, 'tab2')
          


          # print(xls)
          # print(df1.to_numpy()[34][0])
          # print(len(df1))
          # print(df1['nickname'][0])
          # print(df1['nickname'])
          # print(df1.columns.tolist())


          t = len(df1)
          a = 0
          primeiro =[]
          segundo = []

          for cliente in clientes:

              primeiro.append(str(cliente.nickname))

              if a < t:
                  segundo.append(str(df1.to_numpy()[a][0]))

              a += 1

          def Diff(li1, li2):
              return list(set(li1) - set(li2))

          # Inativa Cliente
          # print(Diff(primeiro, segundo))

          inativos = Diff(primeiro, segundo)

          for x in inativos:
              Clientes.objects.filter(nickname=x).update(
                  status='Inativo',
                  data_registro=data_em_texto
              )

          for data in df1.to_numpy():
              # print(data)
              if len(Clientes.objects.filter(nickname=data[0])) == 1:

                  if str(Clientes.objects.filter(nickname=data[0])[0].assessor) != str(data[2]):
                      Clientes.objects.filter(nickname=data[0]).update(
                          nome=str(data[1]).title(),
                          assessor=data[2],
                          antigo_assessor=Clientes.objects.filter(nickname=data[0])[0].assessor,
                          d0=data[3],
                          d1=data[4],
                          d2=data[5],
                          d3=data[6],
                          d4=data[7],
                          troca='interna',
                          data_registro=data_em_texto
                      )
                  else:

                      Clientes.objects.filter(nickname=data[0]).update(
                          nome=str(data[1]).title(),
                          d0=data[3],
                          d1=data[4],
                          d2=data[5],
                          d3=data[6],
                          d4=data[7],
                          data_registro=data_em_texto
                      )
              else:
                  value = Clientes(
                      nickname=data[0],
                      nome=str(data[1]).title(),
                      assessor=data[2],
                      d0=data[3],
                      d1=data[4],
                      d2=data[5],
                      d3=data[6],
                      d4=data[7],
                      status='Novo',
                      data_registro=data_em_texto
                  )
                  value.save()
              sleepy(1)

          df2 = pd.read_excel(xls, 'tab1')
          for data in df2.to_numpy():
              # print(data)

              if len(Clientes.objects.filter(nickname=data[1])) == 1 and  len(data[3]) > 1 and data[7] == 'CONCLUÍDO':
                  Clientes.objects.filter(nickname=data[1]).update(
                          # nome=str(data[1]).title(),
                          assessor=data[3].split('-')[0].replace(" ", ""),
                          # antigo_assessor=Clientes.objects.filter(nickname=data[0])[0].assessor,
                          # d0=data[3],
                          # d1=data[4],
                          # d2=data[5],
                          # d3=data[6],
                          # d4=data[7],
                          troca='externa',
                          status='Novo',
                          data_registro=data[6]
                      )
              elif len(data[3]) > 1 and data[7] == 'CONCLUÍDO':
                  value = Clientes(
                      nickname=data[1],
                      # nome=str(data[1]).title(),
                      assessor=data[3].split('-')[0].replace(" ", ""),
                      # d0=data[3],
                      # d1=data[4],
                      # d2=data[5],
                      # d3=data[6],
                      # d4=data[7],
                      troca='externa',
                      status='Novo',
                      data_registro=data[6]
                  )
                  value.save()
              sleepy(1)

      return True  

  except Exception as e:
    print(e)           