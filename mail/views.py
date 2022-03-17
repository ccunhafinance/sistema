import json

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from clients.models import Espelhamento
from mail.models import Categoria, EmailCategoria
from users.models import CustomUser, UserProfile
from django.views.decorators.csrf import requires_csrf_token

from django.contrib import messages
from tablib import Dataset
from datetime import date
import datetime
# from .models import EmailCategoria

main_icon = 'fal fa-envelope'

# view
def mail_list(request, num=0):
    categorias = Categoria.objects.all()

    context = {
        'num': num,
        'categorias': categorias,
        # Crumbs First Page Config
        'first_page_name': 'Mail',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': '',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': '',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': '',
        'subtitle': 'Mail',
        'sticker': 'Novo',
        'page_description': 'Listagem de as categorias de E-mails'
    }

    return render(request, 'mail/list_view.html', context)

# view
def add_template(request, num=0, var=0):

    context = {
        'num':num,
        'var':var,
        # Crumbs First Page Config
        'first_page_name': 'Mail',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Adicionar Template',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': '',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': '',
        'subtitle': 'Mail',
        'sticker': 'Novo',
        'page_description': 'Adicionar Template'
    }

    return render(request, 'mail/template_view.html', context)

# view
def edit_template(request, num=0, var=0):

    template = EmailCategoria.objects.get(id=num)


    # print(template[0])

    context = {
        'template':template,
        'var':var,
        # Crumbs First Page Config
        'first_page_name': 'Mail',
        'first_page_link': 'mail',
        # Crumbs Second Page Config
        'second_page_name': 'Editar Template',
        'second_page_link': 'mail',
        # Crumbs Third Page Config
        'third_page_name': '',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': '',
        'subtitle': 'Mail',
        'sticker': 'Novo',
        'page_description': 'Editar Template'
    }

    return render(request, 'mail/template_edit.html', context)

def template_preview(request, pk):
    template = EmailCategoria.objects.get(id=pk)


    context = {
        'template':template
    }

    return render(request, 'mail/template_preview.html', context)

# method
def cadastrar_template(request):
    data_atual = datetime.datetime.now()
    data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

    data = EmailCategoria(
        EmailCategoria_id=request.POST['id'],
        nome=request.POST['nome'],
        assunto=request.POST['assunto'],
        titulo=request.POST['titulo'],
        cabecalho=request.POST['cabecalho'],
        body=request.POST['body'],
        criado_por=request.user.id,
        data_insert=data_em_texto,
    )

    data.save()

    return redirect(reverse('mail:template-view', kwargs={'num':request.POST['id'], 'var':1 }))

# method
def save_edit_template(request):
    data_atual = datetime.datetime.now()
    data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

    EmailCategoria.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        nome=request.POST['nome'],
        assunto=request.POST['assunto'],
        titulo=request.POST['titulo'],
        cabecalho=request.POST['cabecalho'],
        body=request.POST['body'],
        editado_por=request.user.id,
        data_edited=data_em_texto,
    )



    return redirect(reverse('mail:template-edit', kwargs={'num':request.POST['id'], 'var':1 }))

# method
def add_categoria(request):
    data_atual = datetime.datetime.now()
    data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

    categorias = Categoria.objects.filter(nome=request.POST['nome'].lower())

    a = len(categorias)

    if a == 1:
        return redirect(reverse('mail:mail-list-error', args='1'))
    else:

        value = Categoria(
            nome=request.POST['nome'],
            criado_por=request.user.id,
            editado_por=request.user.id,
            data_insert=data_em_texto,
        )
        value.save()

        return redirect(reverse('mail:mail-list', args='2'))

# method
def edit_categ(request):
    data_atual = datetime.datetime.now()
    data_em_texto = data_atual.strftime('%d/%m/%Y %H:%M:%S')

    Categoria.objects.filter(id=request.POST['id']).update(
        id=request.POST['id'],
        nome=request.POST['nome'],
        editado_por=request.user.id,
        data_edited=data_em_texto
    )

    return redirect(reverse('mail:mail-list', args='4'))

# method
def delete_template(request, num):
    data = Categoria(id=num)
    data.delete()

    return redirect(reverse('mail:mail-list', args='3'))

# method
def delete_template_one(request, num):
    data = EmailCategoria(id=num)
    data.delete()

    return redirect(reverse('mail:mail-list', args='9'))

# method return real time
def get_category_templates(request):
    templates = EmailCategoria.objects.all()

    id = request.POST['choice']

    print(id)

    response = ['<tr>' \
                    '<td>' +
                        '<a href="'+reverse('mail:template-view', kwargs={'num':id})+'" class="text-success"><i class="fal fa-file-plus"></i> Adicionar Template</a>' +
                    '</td>'+
                    '<td>'+
                        '<a href="#" onClick="change_categ_name('+str(id)+')" data-toggle="modal" data-target="#editar-categoria" class="text-warning"><i class="fal fa-file-edit"></i> Editar Categoria</a> | <a href="javascript:void(0);" id="js-sweetalert2-example-8" class="text-danger"><i class="fal fa-file-excel"></i> Excluir Categoria</a> <input hidden id="id_category" value="'+id+'"><input hidden id="categ_name" value="">'
                    '</td>'

                '</tr>'+'<tr><td><hr></td><td><hr></td></tr>'

                ]
    #

    for temp in templates:

        print(temp.EmailCategoria_id)
        if str(temp.EmailCategoria_id) == str(id):
            response.append(
                            '<tr>' \
                                '<td><a href="'+reverse('mail:template_preview',kwargs={'pk':temp.id})+'" target="_blank">' + str(temp.nome) + '</td>' '<td>'+
                        '<a href="'+reverse('mail:template-edit', kwargs={'num':temp.id,'var':0})+'" class="text-warning"><i class="fal fa-file-edit"></i> Editar Template</a> | <a href="#" onClick="dell_temp('+str(temp.id)+')" class="text-danger"><i class="fal fa-file-excel"></i> Excluir Template</a>'
                    '</td>'+
                            '</tr>'



            )

    return HttpResponse(response)
