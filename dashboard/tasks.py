from celery import shared_task
from django.core.mail import send_mail
from time import sleep
from core.celery import app
import datetime
from clients.models import *
from datetime import date
from django.core.mail import EmailMessage
from mail.models import *



@shared_task
def sleepy(duration):
    sleep(duration)
    return None

@app.task(name='send_email_teste')
def send_email_teste():

    try:
        # time_thresold = datetime.now() - datetime.timedelta(hours=2)
        # all_emails_to_send = NovoEmail.objects.filter(status='n',data_futuro=date.today())
        all_emails_to_send = NovoEmail.objects.filter(status='n')

        sleepy(15)
        for a_email in all_emails_to_send:
            # send_mail('Email 2', 'teste', 'emaildocis@gmail.com', ['cevan83889@xindax.com'])

            dados = EmailCategoria.objects.filter(id=a_email.id_email)

            html_content = dados[0].body
            refresh =html_content.replace('[FNAME]', Clientes.objects.get(id=a_email.cliente_id).nome)
            refresh =refresh.replace('[CODCLIENTE]', Clientes.objects.get(id=a_email.cliente_id).nickname)
            sexo = Clientes.objects.get(id=a_email.cliente_id).sexo
            if sexo == 'M':
                n_sexo = 'bem vindo'
            else:
                n_sexo = 'bem vinda'
            refresh =refresh.replace('[TEXT1]', n_sexo)


            email = EmailMessage(
                dados[0].nome,
                # 'Renda Fixa',
                refresh,
                'Inove Investimentos <web@inoveinvestimentos.com.br>',
                ['ccunhafinance@hotmail.com',],
                # ['ccunhafinance@gmail.com','bruno.martins@inoveinvestimentos.com.BR'],
                reply_to=['ondemand@inoveinvestimentos.com.br'],
                # headers={'Message-ID': 'foo'},
            )
            email.content_subtype = "html"
            email.send()

            NovoEmail.objects.filter(id=a_email.id).update(
                status='OK',
            )


        return None

    except Exception as e:
        print(e)





