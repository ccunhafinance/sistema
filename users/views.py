from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, TemplateView
from django.urls import reverse_lazy
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic



main_icon = 'fal fa-key'

class MyPasswordChangeView(LoginRequiredMixin,PasswordChangeView):
    template_name = 'users/change_view.html'
    success_url = reverse_lazy('users:pass-check')


class MyPasswordChangeDoneView(LoginRequiredMixin,PasswordChangeDoneView):
    template_name = 'users/done_view.html'

    def get_context_data(self, **kwargs):
        context = {
            # Crumbs First Page Config
            'first_page_name': 'Senha',
            'first_page_link': 'users:alterar-senha',
            # Crumbs Second Page Config
            'second_page_name': 'Senha Alterada',
            'second_page_link': '',
            # Crumbs Third Page Config
            'third_page_name': '',
            'third_page_link': '',
            # Current Page
            'icon': main_icon,
            'page_name': 'Senha Alterada',
            'subtitle': '',
            'sticker': '',
        }

        return context

@login_required(login_url='/')
def pass_check(request):

    CustomUser.objects.filter(id=request.user.id).update(has_pass=True)


    return redirect('/usuarios/alterar-senha/alterada/')

pro_icon = 'fal fa-id-card-alt'

