import json
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.http import HttpResponse
# import requests
from users.models import CustomUser
from clients.models import *
from offers.models import EmailIpo, OfferRvIpo, EmailRf, OfferRf
import numpy as np
from datetime import datetime
from pytz import timezone
from django.contrib.auth.decorators import login_required


def get_client(request):
    # with open('data/clientes/clientes.txt', encoding='latin-1') as json_file:
    #     clientes = json.load(json_file)

    clientes = Clientes.objects.all()

    code = request.POST['code']
    # code = '71057'
    # CODIGO_XP_CLIENTE
    # ': 2304734
    usuarios = CustomUser.objects.all()
    espelhamento = Espelhamento.objects.filter(assessor_permited=request.user.id)

    espelhados = [request.user.codigo]
    for usuario in usuarios:
        for espelho in espelhamento:
            if usuario.id == espelho.assessor_id:
                espelhados.append(usuario.codigo)

    clientes_de = np.array(espelhados)
    permitidos = np.array_split(clientes_de, 1)

    all_clients_to_check = []
    for permission in permitidos:
        for cliente in clientes:
            if permission == cliente.assessor:
                all_clients_to_check.append(cliente)

    # print(all_clients_to_check)

    response = ''
    for i in all_clients_to_check:
        if int(i.nickname) == int(code):
            # nome = i['PRIMEIRO_NOME_CLIENTE']

            assessor_owner = CustomUser.objects.get(codigo=i.assessor)

            assessor_permited = str(i.assessor)+ ' - '+ str(assessor_owner.first_name)+ ' ' + str(assessor_owner.last_name) + ' - ' + str(assessor_owner.email)
            code_name_last = str(i.assessor)+ ' - '+ str(assessor_owner.first_name)+ ' ' + str(assessor_owner.last_name)
            assessor_responsavel = str(i.assessor)

          

            response = '<input hidden id="got_name" value="'+str(i.nome.capitalize().split()[0])+'">' \
                       '<input hidden id="got_email" value="'+str(i.email)+'">' \
                       '<input hidden id="got_assessor_owner" value="'+assessor_permited+'">' \
                       '<input hidden id="code_name_last" value="'+code_name_last+'">' \
                       '<input hidden id="got_responsavel" value="'+assessor_responsavel+'">' \

            break
        else:
            response = 'false'

    return HttpResponse(response)

# Ofertas RV IPO

def send_mail_ipo(request):
    html_content = request.POST['email_body']

    email = EmailMessage(
        request.POST['assunto'],
        # 'Renda Fixa',
        html_content,
        'Inove Investimentos <web@inoveinvestimentos.com.br>',
        [request.POST['email']],
        reply_to=['ordens@inoveinvestimentos.com.br'],
        headers={'Message-ID': 'foo'},
    )
    email.content_subtype = "html"
    if email.send():

        if request.POST['preMax'] == '' or request.POST['preMax'] == 'R$ 0,00':
            premax = 'A Mercado'
        else:
            premax = request.POST['preMax']

        remetente = request.POST['remetente']

        data = EmailIpo(
            id_oferta=OfferRvIpo.objects.get(pk=request.POST['chave']),
            assessor_responsavel=request.POST['assessor_responsavel'],
            id_sender=request.user.id,
            nome_oferta=request.POST['nome_oferta'],
            remetente=remetente.split('-')[0].replace(' ',''),
            codigo_cliente=request.POST['codigo'],
            nome_cliente=request.POST['nome'],
            modalidaade=request.POST['modalidaade'],
            vinculo=request.POST['vinculo'],
            valFim=request.POST['valFim'],
            preMax=premax,
            email_body=request.POST['email_body'],
            email=request.POST['email'],
            assunto=request.POST['assunto'],
        )

        data.save()

        response = "Email enviado"
    else:
        response = 'false'

    # Redirect to same page after form submit
    return HttpResponse(response)

def get_mail_ipo(request):

    usuario = CustomUser.objects.get(id=request.user.id)

    emails_enviados = EmailIpo.objects.filter(id_oferta_id=request.POST['pk'])

    # print(request.user.id)

    response= []

    if len(emails_enviados) > 0:
        for i in emails_enviados:
            quem_mandou = CustomUser.objects.get(id=i.id_sender)
            the_remetente = CustomUser.objects.get(codigo=i.remetente)
            if str(quem_mandou.codigo) == str(usuario.codigo) or str(i.assessor_responsavel) == str(usuario.codigo):
                fuso_horario = timezone('America/Sao_Paulo')
                data_fuso = i.data_sent.astimezone(fuso_horario)
                response.append('<tr>'\
                                    '<td><a href="/ofertas/rv/ipo/email-enviado-rv-ipo/'+str(i.id)+'/"><i class="fal fa-envelope-open-text"></i></td>'\
                                    '<td>' + str(i.codigo_cliente) + ' - ' + str(i.nome_cliente) + '</td>'\
                                    '<td>' + str(quem_mandou.codigo) +' - ' +str(quem_mandou.first_name)+ ' ' +str(quem_mandou.last_name)+ '</td>'\
                                    '<td>' + str(i.remetente) +' - '+the_remetente.first_name+ ' '+ the_remetente.last_name+ '</td>'\
                                    '<td>' + str(i.email) + '</td>'\
                                    '<td>' + str(i.modalidaade) + '</td>'\
                                    '<td>' + str(i.vinculo) + '</td>'\
                                    '<td>' + str(i.valFim) + '</td>'\
                                    '<td>' + str(i.preMax) + '</td>'\
                                    '<td>' + str(data_fuso.strftime('%d/%m/%Y - %H:%M')) + '</td>'\
                                '</th>')
            

    else:

        response = 'Nenhum email enviado ate o momento'

    return HttpResponse(response)

# Ofertas RF

@login_required(login_url='/')
def send_mail_rf(request):
    html_content = request.POST['assunto']

    print(html_content)

    email = EmailMessage(
        request.POST['assunto'],
        # 'Renda Fixa',
        html_content,
        'Inove Investimentos <web@inoveinvestimentos.com.br>',
        [request.POST['email'],],
        reply_to=['ordens@inoveinvestimentos.com.br'],
        headers={'Message-ID': 'foo'},
    )
    email.content_subtype = "html"


    email.send()

    response = 'ok'



    # if email.send():

    #     remetente = request.POST['remetente']

    #     print(request.POST['email_body'])

    #     data = EmailRf(
    #         id_oferta=OfferRf.objects.get(pk=request.POST['chave']),
    #         assessor_responsavel=request.POST['assessor_responsavel'],
    #         id_sender=request.user.id,
    #         nome_oferta=request.POST['nome_oferta'],
    #         remetente=remetente.split('-')[0].replace(' ',''),
    #         codigo_cliente=request.POST['codigo'],
    #         nome_cliente=request.POST['nome'],
    #         serie=request.POST['serie'],
    #         taxa=request.POST['taxa'],
    #         valor=request.POST['valor'],
    #         email_body=html_content,
    #         email=request.POST['email'],
    #         assunto=request.POST['assunto'],
    #     )

    #     data.save()

    #     response = "Email enviado"
    # else:
    #     response = 'false'

    # Redirect to same page after form submit
    return HttpResponse(response)

def get_mail_rf(request):
    usuario = CustomUser.objects.get(id=request.user.id)

    emails_enviados = EmailRf.objects.filter(id_oferta_id=request.POST['pk'])

    # print(request.user.id)

    response = []

    if len(emails_enviados) > 0:
        for i in emails_enviados:
            quem_mandou = CustomUser.objects.get(id=i.id_sender)
            the_remetente = CustomUser.objects.get(codigo=i.remetente)
            if str(quem_mandou.codigo) == str(usuario.codigo) or str(i.assessor_responsavel) == str(usuario.codigo):
                fuso_horario = timezone('America/Sao_Paulo')
                data_fuso = i.data_sent.astimezone(fuso_horario)

                serie = i.serie.split('+')


                response.append('<tr>' \
                                    '<td><a href="/ofertas/rf/email-enviado-rf/' + str(i.id) + '/"><i class="fal fa-envelope-open-text"></i></td>' \
                                    '<td>' + str(i.codigo_cliente) + ' - ' + str(i.nome_cliente) + '</td>' \
                                    '<td>' + str(quem_mandou.codigo) + ' - ' + str(quem_mandou.first_name) + ' ' + str(quem_mandou.last_name) + '</td>' \
                                    '<td>' + str(i.remetente) + ' - ' + the_remetente.first_name + ' ' + the_remetente.last_name + '</td>' \
                                    '<td>' + str(i.email) + '</td>' \
                                    '<td>' + str(serie[0]) + '</td>' \
                                    '<td>' + str(serie[1]+' + '+serie[2]+' + '+serie[3]) + '</td>' \
                                    '<td>' + str(serie[1]+' + '+i.taxa) + '</td>' \
                                    '<td>' + str(i.valor) + '</td>' \
                                    '<td>' + str(data_fuso.strftime('%d/%m/%Y - %H:%M')) + '</td>' \
                                '</th>')


    else:

        response = 'Nenhum email enviado ate o momento'

    return HttpResponse(response)

