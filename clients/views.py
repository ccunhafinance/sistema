import json

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from clients.models import Espelhamento, NovoEmail, RegistroAtividades
from users.models import CustomUser, UserProfile

from .models import Clientes
from mail.models import *
from .resources import ClientesResources
from django.contrib import messages
from tablib import Dataset
from datetime import date
from datetime import timedelta, date
import datetime

main_icon = 'ni ni-users'


def google_sheets(request):
    UserProfile.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        google_sheets=request.POST['google_sheets']
    )

    return redirect(reverse('clients:clients-list'))

def delet_all(request):
    clientes = Clientes.objects.all()

    for cliente in clientes:

        data = Clientes(id=cliente.id)
        data.delete()

    return redirect(reverse('clients:clients-list'))

def update_troca_assessor(request):
    rotina = request.POST.get('rotina', False)

    if rotina != False:
        rotina = '1'
    else:
        rotina = '0'

    data_atual = datetime.datetime.now()
    data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        rotina=rotina,
        # zap_mail=request.POST['zap_mail'],
        status='ok',
        troca='ok',
        cliente_dia='sim',
        data_registro=data_em_texto

    )

    id_categ = Categoria.objects.first()

    print(id_categ.id)

    teste = EmailCategoria.objects.filter(EmailCategoria_id=id_categ)

    dias = date.today() + timedelta(days=0)
    for a in teste:
        # print(a.nome)

        value = NovoEmail(
            cliente_id=request.POST['id'],
            id_email=a.id,
            categ_email_id=id_categ.id,
            data_futuro=dias,
            status='n'

        )
        value.save()

        dias = dias + timedelta(days=7)





    return redirect(reverse('clients:clients-list'))

def update_new_cliente(request):
    rotina = request.POST.get('rotina', False)

    if rotina != False:
        rotina = '1'
    else:
        rotina = '0'

    data_atual = datetime.datetime.now()
    data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        nome=request.POST['nome'],
        sexo=request.POST['sexo'],
        email=request.POST['email'],
        telefone=request.POST['telefone'],
        data_nascimento=request.POST['data_nascimento'],
        rotina=rotina,
        # zap_mail=request.POST['zap_mail'],
        status='ok',
        cliente_dia='sim',
        data_registro=data_em_texto

    )

    return redirect(reverse('clients:clients-list'))

def upload_clientes(request):
    if request.method == 'POST':
        clientes_resource = ClientesResources()
        dataset = Dataset()
        new_cliente = request.FILES['myfile']

        if not new_cliente.name.endswith('xlsx'):
            messages.info('Formato de arquivo não suportado')
            return redirect(reverse('clients:clients-list'))

        imported_data = dataset.load(new_cliente.read(), format='xlsx')

        clientes = Clientes.objects.all()

        data_atual =  datetime.datetime.now()
        data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

        # print (len(clientes))

        if len(clientes)==0:

            for data in imported_data:

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

            t = len(imported_data)
            a = 0
            primeiro =[]
            segundo = []

            for cliente in clientes:

                primeiro.append(str(cliente.nickname))

                if a < t:
                    segundo.append(str(imported_data[a][0]))

                a += 1

            def Diff(li1, li2):
                return list(set(li1) - set(li2))

            # Inativa Cliente
            print(Diff(primeiro, segundo))

            inativos = Diff(primeiro, segundo)

            for x in inativos:
                Clientes.objects.filter(nickname=x).update(
                    status='Inativo',
                    data_registro=data_em_texto
                )

            for data in imported_data:




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
                            troca='existe',
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

    return redirect(reverse('clients:clients-list'))

# funcoes ombording

def change_tipo_contato(request):
    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        zap_mail=request.POST['zap_mail'],
    )

    data = RegistroAtividades(
        cliente_id=Clientes.objects.get(id=request.POST['id']).id,
        registro='Tipo de contato do cliente foi alterado',
        descricao=request.POST['zap_mail'],
        assessor_responsavel=request.user.id
    )
    data.save()

    response ='ok'

    return HttpResponse(response)

def acomp_perm(request):
    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        onbording_acomp_per=request.POST['onbording_acomp_per'],
    )

    if request.POST['onbording_acomp_per'] == 1:
        acomp = 'Desejado'
    else:
        acomp = 'Indesejado'

    data = RegistroAtividades(
        cliente_id=Clientes.objects.get(id=request.POST['id']).id,
        registro='Acompanhamento permnente foi alterado',
        descricao=acomp,
        assessor_responsavel=request.user.id
    )
    data.save()

    response = 'ok'

    return HttpResponse(response)

def acomp_rf(request):
    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        onbording_acomp_rf=request.POST['onbording_acomp_rf'],
    )

    if request.POST['onbording_acomp_rf'] == 1:
        acomp = 'Desejado'
    else:
        acomp = 'Indesejado'

    data = RegistroAtividades(
        cliente_id=Clientes.objects.get(id=request.POST['id']).id,
        registro='Oportunidade RF foi alterado',
        descricao=acomp,
        assessor_responsavel=request.user.id
    )
    data.save()

    response = 'ok'

    return HttpResponse(response)

def acomp_acoes(request):
    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        onbording_acomp_acoes=request.POST['onbording_acomp_acoes'],
    )

    if request.POST['onbording_acomp_acoes'] == 1:
        acomp = 'Desejado'
    else:
        acomp = 'Indesejado'

    data = RegistroAtividades(
        cliente_id=Clientes.objects.get(id=request.POST['id']).id,
        registro='Oportunidade RF foi alterado',
        descricao=acomp,
        assessor_responsavel=request.user.id
    )
    data.save()

    response = 'ok'

    return HttpResponse(response)

def acomp_fii(request):
    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        onbording_acomp_fii=request.POST['onbording_acomp_fii'],
    )

    if request.POST['onbording_acomp_fii'] == 1:
        acomp = 'Desejado'
    else:
        acomp = 'Indesejado'

    data = RegistroAtividades(
        cliente_id=Clientes.objects.get(id=request.POST['id']).id,
        registro='Oportunidade FII foi alterado',
        descricao=acomp,
        assessor_responsavel=request.user.id
    )
    data.save()

    response = 'ok'

    return HttpResponse(response)

def acomp_fiinvest(request):
    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        onbording_acomp_fiinvest=request.POST['onbording_acomp_fiinvest'],
    )

    if request.POST['onbording_acomp_fiinvest'] == 1:
        acomp = 'Desejado'
    else:
        acomp = 'Indesejado'

    data = RegistroAtividades(
        cliente_id=Clientes.objects.get(id=request.POST['id']).id,
        registro='Oportunidade Fundo de Investimento foi alterado',
        descricao=acomp,
        assessor_responsavel=request.user.id
    )
    data.save()

    response = 'ok'

    return HttpResponse(response)

def update_observacao(request):
    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        onbording_obs=request.POST['obs'],
    )


    data = RegistroAtividades(
        cliente_id=Clientes.objects.get(id=request.POST['id']).id,
        registro='O Campo Observação foi alterado',
        descricao=request.POST['obs'],
        assessor_responsavel=request.user.id
    )
    data.save()

    response = 'ok'

    return HttpResponse(response)

def enviar_implement(request):
    data_atual = datetime.datetime.now()
    data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        onbording_impl_envio_sugestao=data_em_texto,
    )


    data = RegistroAtividades(
        cliente_id=Clientes.objects.get(id=request.POST['id']).id,
        registro='Envio de Implementação',
        descricao='-',
        assessor_responsavel=request.user.id
    )
    data.save()

    response = 'ok'

    return HttpResponse(response)

def enviar_sujest(request):
    data_atual = datetime.datetime.now()
    data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        onbording_envio_sugestao=data_em_texto,
    )


    data = RegistroAtividades(
        cliente_id=Clientes.objects.get(id=request.POST['id']).id,
        registro='Envio de Sujestão',
        descricao='-',
        assessor_responsavel=request.user.id
    )
    data.save()

    response = 'ok'

    return HttpResponse(response)

def perfil_preenchido(request):
    data_atual = datetime.datetime.now()
    data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        onbording_perfil_preenchido=data_em_texto,
    )


    data = RegistroAtividades(
        cliente_id=Clientes.objects.get(id=request.POST['id']).id,
        registro='Perfil Ondemand Preenchido',
        descricao='-',
        assessor_responsavel=request.user.id
    )
    data.save()

    response = 'ok'

    return HttpResponse(response)

def cliente_responde(request, id, token):

    cliente = Clientes.objects.get(nickname=id)

    context = {
        'token': token,
        'cliente': cliente
    }

    return render(request, 'clients/questinario.html', context)

def obrigado_questionario(request):

    return render(request, 'clients/obrigado.html')

def send_email_ondemand(request):
    data_atual = datetime.datetime.now()
    data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

    cliente = Clientes.objects.get(id=request.POST['id'])

    codigo = cliente.nickname
    token = hash(codigo)

    body = 'Responda o questionário no link abaixo <br> <a href="'+request.build_absolute_uri('/clientes/questionario/'+str(codigo)+'/'+str(token)+'/')+'">Responder questionário</a>'

    email = EmailMessage(
        'Inove Investimentos | Seu Futuro Positivo',
        # 'Renda Fixa',
        body,
        'Questionário Inove Investimentos <web@inoveinvestimentos.com.br>',
        # ['ccunhafinance@hotmail.com', ],
        ['ccunhafinance@gmail.com','bruno.martins@inoveinvestimentos.com.BR'],
        reply_to=['ondemand@inoveinvestimentos.com.br'],
        headers={'Message-ID': 'foo'},
    )

    email.content_subtype = "html"
    email.send()

    Clientes.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        token=token,
        onbording_email=data_em_texto,
    )

    data = RegistroAtividades(
        cliente_id=Clientes.objects.get(id=request.POST['id']).id,
        registro='Email de questionamento enviado!',
        descricao='-',
        assessor_responsavel=request.user.id
    )
    data.save()

    return HttpResponse('ok')

def save_by_client(request):
    codigo = request.POST['codigo']

    print(Clientes.objects.get(nickname=codigo).id)
    onbording_acomp_acoes = request.POST.get('onbording_acomp_acoes', False)
    onbording_acomp_fii = request.POST.get('onbording_acomp_fii', False)
    onbording_acomp_fiinvest = request.POST.get('onbording_acomp_fiinvest', False)
    onbording_acomp_per = request.POST.get('onbording_acomp_per', False)
    onbording_acomp_rf = request.POST.get('onbording_acomp_rf', False)

    if onbording_acomp_acoes != False:
        onbording_acomp_acoes = 1
    else:
        onbording_acomp_acoes = 0

    onbording_acomp_fii = request.POST.get('onbording_acomp_fii', False)
    if onbording_acomp_fii != False:
        onbording_acomp_fii = 1
    else:
        onbording_acomp_fii = 0

    onbording_acomp_fiinvest = request.POST.get('onbording_acomp_fiinvest', False)
    onbording_acomp_fiinvest = request.POST.get('onbording_acomp_fii', False)
    if onbording_acomp_fiinvest != False:
        onbording_acomp_fiinvest = 1
    else:
        onbording_acomp_fiinvest = 0
    onbording_acomp_per = request.POST.get('onbording_acomp_per', False)
    if onbording_acomp_per != False:
        onbording_acomp_per = 1
    else:
        onbording_acomp_per = 0
    onbording_acomp_rf = request.POST.get('onbording_acomp_rf', False)
    if onbording_acomp_rf != False:
        onbording_acomp_rf = 1
    else:
        onbording_acomp_rf = 0


    Clientes.objects.filter(nickname=codigo).update(
        id=Clientes.objects.get(nickname=codigo).id,

        zap_mail=request.POST['zap_mail'],

        onbording_acomp_acoes=onbording_acomp_acoes,
        onbording_acomp_fii=onbording_acomp_fii,
        onbording_acomp_fiinvest=onbording_acomp_fiinvest,
        onbording_acomp_per=onbording_acomp_per,
        onbording_acomp_rf=onbording_acomp_rf,

        onbording_obs=request.POST['onbording_obs'],
        token='false'

    )


    if onbording_acomp_per == 1:
        a = 'sim'
    else:
        a = 'Não'

    if onbording_acomp_rf == 1:
        b = 'sim'
    else:
        b = 'Não'

    if onbording_acomp_fiinvest == 1:
        c = 'sim'
    else:
        c = 'Não'

    if onbording_acomp_acoes == 1:
        d = 'sim'
    else:
        d = 'Não'

    if onbording_acomp_fii == 1:
        e = 'sim'
    else:
        e = 'Não'


    dados = ' - Meio de comunicação: '+request.POST['zap_mail']+'<br>'+\
            '- Acompanhamento Permanente: '+a+\
            '<br>- Oportunidades de Renda Fixa: '+b+\
            '<br>- Oportunidades de Fundos de Investimentos: '+c+\
            '<br>- Oportunidades de Ações: '+d+\
            '<br>- Oportunidades de Fundos Imobiliários: '+e+\
            '<br>- Observações: <br>'+request.POST['onbording_obs']



    data = RegistroAtividades(
        cliente_id=Clientes.objects.get(nickname=codigo).id,
        registro='Questionário respondido Pelo cliente',
        descricao=dados,
        assessor_responsavel=Clientes.objects.get(nickname=codigo).assessor
    )
    data.save()

    email = EmailMessage(
        'Questinário respondido',
        # 'Renda Fixa',
        'O Cliente '+codigo+' respondeu o questionário!',
        'Questionário Respondido <web@inoveinvestimentos.com.br>',
        # ['ccunhafinance@hotmail.com', ],
        ['ccunhafinance@gmail.com', 'bruno.martins@inoveinvestimentos.com.BR'],
        reply_to=['ondemand@inoveinvestimentos.com.br'],
        headers={'Message-ID': 'foo'},
    )

    email.content_subtype = "html"
    email.send()

    return redirect(reverse('clients:obrigado-questionario'))


class ListViewClients(LoginRequiredMixin, generic.TemplateView):
    template_name = "clients/list_view.html"
    login_url = '/'

    # id_categ = Categoria.objects.first()
    #
    # print(id_categ)
    #
    # teste = EmailCategoria.objects.filter(EmailCategoria_id=id_categ)
    #
    # for a in teste:
    #     print (a.nome)




    def get_context_data(self, **kwargs):

        # Load Clients based on the internal files
        # with open('data/clientes/clientes.txt', encoding='latin1') as json_file:
        #     clientes = json.load(json_file)

        # load Clients from DB

        # print(self.request.user.id)

        assessores = CustomUser.objects.all()

        f = ''
        for assessor in assessores:
            if assessor.id == self.request.user.id:
                f = assessor.codigo

        # print(f)

        onbording = Clientes.objects.filter(rotina="1")
        n_onboarding = len(onbording)

        clientes = Clientes.objects.filter(assessor=f)
        n_clientes = len(clientes)
        novos_clientes = Clientes.objects.filter(status='Novo',assessor=f)
        inativo = Clientes.objects.filter(status='Inativo',assessor=f)
        google = Clientes.objects.filter(cliente_dia='sim', assessor=f)
        n_contatos = len(Clientes.objects.filter(cliente_dia='sim', assessor=f))
        n_inativo = len(inativo)
        n_novos_clientes = len(novos_clientes)

        i = Clientes.objects.filter(troca='existe',assessor=f)

        num_clientes_ativos = int(len(clientes)) - int(len(inativo))

        troca = len(i)

        context = {
            'n_onboarding': n_onboarding,
            'onbording': onbording,
            'clientes': clientes,
            'n_clientes': n_clientes,
            'inativo': inativo,
            'n_inativo': n_inativo,
            'novos_clientes': novos_clientes,
            'n_novos_clientes': n_novos_clientes,
            'n_troca_assessor': troca,
            'troca_assessor': i,
            'contatos': google,
            'n_contatos': n_contatos,
            'num_clientes_ativos': num_clientes_ativos,
            # Crumbs First Page Config
            'first_page_name': 'Clientes',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Meus Clientes',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': '',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Clientes',
            'subtitle': 'Meus Clientes',
            'sticker': 'Novo',
            'page_description': 'Listagem de todos os meus clientes.'
        }

        return context

# ------------

class ListMirrorView(LoginRequiredMixin, generic.TemplateView):
    template_name = "clients/mirror_view.html"
    login_url = '/'

    def get_context_data(self, **kwargs):

        clientes = Clientes.objects.all()

        context = {
            'clientes': clientes,
            'espelhamento': Espelhamento.objects.all(),
            'usuarios': CustomUser.objects.filter(type='assessor'),
            # Crumbs First Page Config
            'first_page_name': 'Clientes',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Espelhamento',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': '',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Espelhamento',
            'subtitle': '',
            'sticker': 'Novo',
            'page_description': 'Listagem de clientes espelhados.'
        }

        return context

def rotina_emails(request, id):

    emails_cliente = NovoEmail.objects.filter(cliente_id=id)

    context = {
        'emails_cliente':emails_cliente,
        # Crumbs First Page Config
        'first_page_name': 'Clientes',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Rotina de emails',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': '',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Rotina',
        'subtitle': '',
        'sticker': 'Novo',
        'page_description': 'Listagem de clientes espelhados.'
    }

    return render(request, 'clients/rotina_view.html', context)

def mirroradd(request):
    if request.method == 'POST':
        data = Espelhamento(
            assessor=CustomUser.objects.get(id=request.user.id),
            assessor_permited=request.POST['assessor_permited']
        )

        data.save()

        return redirect(reverse('clients:mirror-list'))

def mirrordelete(request, pk):
    data = Espelhamento(
        id=pk,
    )
    data.delete()

    return redirect(reverse('clients:mirror-list'))

def get_cliente_data(request):
    clientes = Clientes.objects.all()


    code = request.POST['code']

    response = []
    for cliente in clientes:
        if cliente.assessor == code:

            response.append( '<tr>' \
                           '<td>'+ str(cliente.nickname) + '</td>'\
                           '<td>'+ str(cliente.nome) + '</td>'\
                           '<td>'+ '<a href="mailto:'+str(cliente.email)+'">'+str(cliente.email)+'</a>' + '</td>'\
                       '</th>')




    return HttpResponse(response)

