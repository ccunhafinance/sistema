from django import forms
from .models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
import re

class OfferRvIpoForm(forms.ModelForm):
    class Meta:
        model = OfferRvIpo
        fields = "__all__"
        widgets = {
            'start_per_res': forms.DateInput(attrs={'type': 'date'}),
            'end_per_res': forms.DateInput(attrs={'type': 'date'}),
            'end_vinc': forms.DateInput(attrs={'type': 'date'}),
            'book': forms.DateInput(attrs={'type': 'date'}),
            'star_neg': forms.DateInput(attrs={'type': 'date'}),
            'liquid': forms.DateInput(attrs={'type': 'date'}),
        }

class ModalidadeIpoForm(forms.ModelForm):

    # amort_beg = forms.DateField(label='Início da Amortização', widget=forms.TextInput(attrs={'type':'date'}))
    # jurus = forms.CharField(label='Jurus')
    # current_tax = forms.CharField(label='Taxa Atual Aproximada')
    # obs = forms.CharField(label='Observações', required=False, widget=forms.Textarea(attrs={'placeholder': 'Observaçoões'}))

    class Meta:
        model = SerieRf
        fields = "__all__"
        widgets = {
            'lock_end': forms.DateInput(attrs={'type': 'date'}),
            # 'end_reserv': forms.DateInput(attrs={'type': 'date'}),
            # 'bookbuilding': forms.DateInput(attrs={'type': 'date'}),
            # 'liquid': forms.DateInput(attrs={'type': 'date'}),
        }

class OfferRfForm(forms.ModelForm):
    # about_comp = forms.CharField(label='Sobre a Empresa', widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}))

    class Meta:
        model = OfferRf
        fields = "__all__"
        widgets = {
            'start_reserv': forms.DateInput(attrs={'type': 'date'}),
            'end_reserv': forms.DateInput(attrs={'type': 'date'}),
            'bookbuilding': forms.DateInput(attrs={'type': 'date'}),
            'liquid': forms.DateInput(attrs={'type': 'date'}),
            'about_comp': forms.Textarea(attrs={'class': 'summernote'}),
            'invet_min': forms.TextInput(attrs={'onkeyup': 'formatCash(this)'}),

        }

class SeriesRfForm(forms.ModelForm):
    # tipe = forms.CharField(label='Série',)
    # tax_top = forms.CharField(label='Taxa Teto',widget=forms.TextInput(attrs={'value':'NTNB ano + '}))
    # tax_ref = forms.CharField(label='Taxa Referêncial',)
    # venciment = forms.CharField(label='Vencimento')
    # duration = forms.CharField(label='Duration (em anos)')
    # amort = forms.CharField(label='Amortização')
    amort_beg = forms.DateField(label='Início da Amortização', widget=forms.TextInput(attrs={'type':'date'}))
    jurus = forms.CharField(label='Juros')
    current_tax = forms.CharField(label='Taxa Atual Aproximada')
    obs = forms.CharField(label='Observações', required=False, widget=forms.Textarea(attrs={'placeholder': 'Observaçoões'}))

    class Meta:
        model = SerieRf
        fields = "__all__"
        widgets = {
            'venciment': forms.DateInput(attrs={'type': 'date'}),
            'tax_ref': forms.TextInput(attrs={'onkeyup': 'formatPercent(this)'}),
            # 'end_reserv': forms.DateInput(attrs={'type': 'date'}),
            # 'bookbuilding': forms.DateInput(attrs={'type': 'date'}),
            # 'liquid': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_tax_top(self, *args, **kwargs):
        tax_top = self.cleaned_data.get('tax_top')

        y = tax_top.split(" ")
        # y = x.split(' ')

        print(len(y))

        if len(y) > 2:
            ntnb = y[0]
            data = y[1]
            mais = y[2]
            print(ntnb)
            print(data)
            print(mais)

            def has_numbers(inputString):
                if len(inputString) == 4 and inputString.isdigit():
                    return True

            if ntnb == 'NTNB' and has_numbers(data) and mais == '+' in tax_top:
                return tax_top
            else:
                raise forms.ValidationError('Taxa Teto deve conter NTNB ano + ')

        raise forms.ValidationError('Taxa Teto deve conter NTNB ano + ')

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = OfferRvSubscription
        fields = "__all__"
        widgets = {
            'mkt_price_date': forms.DateInput(attrs={'type': 'date'}),
            'dir_price_date': forms.DateInput(attrs={'type': 'date'}),
            'start_deal_dir': forms.DateInput(attrs={'type': 'date'}),
            'end_deal_dir': forms.DateInput(attrs={'type': 'date'}),
            'start_reser': forms.DateInput(attrs={'type': 'date'}),
            'end_reser': forms.DateInput(attrs={'type': 'date'}),
            'liquid': forms.DateInput(attrs={'type': 'date'}),
            'date_ex': forms.DateInput(attrs={'type': 'date'}),
        }

class FiiEditForm(forms.ModelForm):
    class Meta:
        model = FiiEdit
        fields = "__all__"
        widgets = {


            'data_base': forms.DateInput(attrs={'type': 'date'}),
            'inicio_periodo_de_negociacao': forms.DateInput(attrs={'type': 'date'}),
            'fim_periodo_de_negociacao': forms.DateInput(attrs={'type': 'date'}),
            'inicio_periodo_preferencia': forms.DateInput(attrs={'type': 'date'}),
            'fim_periodo_preferencia': forms.DateInput(attrs={'type': 'date'}),
            'liquidacao_periodo_preferencia': forms.DateInput(attrs={'type': 'date'}),
            'inicio_periodo_sobra': forms.DateInput(attrs={'type': 'date'}),
            'fim_periodo_sobra': forms.DateInput(attrs={'type': 'date'}),
            'liquidacao_periodo_sobra': forms.DateInput(attrs={'type': 'date'}),
            'inicio_periodo_publico': forms.DateInput(attrs={'type': 'date'}),
            'fim_periodo_publico': forms.DateInput(attrs={'type': 'date'}),
            'liquidacao_periodo_publico': forms.DateInput(attrs={'type': 'date'}),
        }