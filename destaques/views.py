from django.shortcuts import render

main_icon = 'fal fa-stars'

# PAGINA PRINCIPAL SEGURO
def pageDestaqueRendaFixa(request):

    context = {
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
