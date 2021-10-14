from django.shortcuts import render
from django.views import generic
from users.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin


main_icon = 'fal fa-address-card'

# Create your views here.
class ListViewAssessores(LoginRequiredMixin, generic.TemplateView):
    template_name = "assessores/list_view.html"
    login_url = '/'

    def get_context_data(self, **kwargs):

        context = {
            'assessores': CustomUser.objects.filter(type='assessor'),
            # Crumbs First Page Config
            'first_page_name': 'Assessores',
            'first_page_link': '',
            # Crumbs Second Page Config
            'second_page_name': '',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': '',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Assessores',
            'subtitle': 'Assessores',
            'sticker': 'Novo',
            'page_description': 'Listagem de todos os assessores.'
        }

        return context