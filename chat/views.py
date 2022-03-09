from django.shortcuts import render

# Gbobal Variables
main_icon = 'ni ni-tag'

# Create your views here.
def messages_view(request):
    context = {

        # Crumbs First Page Config
        'first_page_name': 'Chat',
        'first_page_link': '',
        # Crumbs Second Page Config
        'second_page_name': '',
        'second_page_link': '',
        # Crumbs Third Page Config
        'third_page_name': '',
        'third_page_link': '',
        # Current Page
        'icon': main_icon,
        'page_name': 'Chat',
        'subtitle': '',
        'sticker': 'Novo',
        'page_description': 'Portal de comunicação interna Inove Investimentos'
    }

    return render(request, 'chat/messages_view.html', context)