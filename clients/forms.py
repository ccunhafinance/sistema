from django import forms
from . models import Clientes

class ModalForm(forms.ModelForm):

    nome = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'type':'Text'}))
    sexo = forms.ChoiceField(label='Sexo', choices=(('F','F'),('M','M')))
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'type':'email'}))
    telefone = forms.CharField(label='Telefone', widget=forms.TextInput(attrs={'type':'text'}))
    data_nascimento = forms.DateField(label='Data de Nascimento', widget=forms.TextInput(attrs={'type':'date'}))
    jaContactei = forms.CharField(label='Cliente ja foi contactado?', widget=forms.CheckboxInput(attrs={'type':'checkbox'}))
    
    class Meta:
        model = Clientes
        fields = ['nome', 'sexo', 'email', 'telefone', 'data_nascimento', 'jaContactei']
       

