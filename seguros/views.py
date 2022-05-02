from django.shortcuts import render

main_icon = 'fal fa-heartbeat'

# PAGINA PRINCIPAL SEGURO
def mainPageSeguro(request):

    context = {
        # Crumbs First Page Config
        'first_page_name': 'Seguro de Vida',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': 'Seguro de Vida',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': '',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Seguro de Vida',
        'subtitle': '',
        'sticker': 'Novo',
        'page_description': ''
    }

    return render(request, 'seguros/main/base.html', context)
