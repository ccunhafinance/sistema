from django.urls import path
from .views import MyPasswordChangeView, MyPasswordChangeDoneView
from .import views

app_name = 'users'
main_icon = 'fal fa-key'

context = {
            # Crumbs First Page Config
            'first_page_name': 'Senha',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': 'Alterar Senha',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': '',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Alterar Senha',
            'subtitle': '',
            'sticker': '',
        }

urlpatterns = [
    path('alterar-senha/', MyPasswordChangeView.as_view(extra_context=context), name='change-password'),
    path('alterar-senha/alterada/', MyPasswordChangeDoneView.as_view(), name='done-password'),
    path('pass-check/', views.pass_check, name='pass-check')

]