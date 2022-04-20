from datetime import date

from django.db import models
from users.models import CustomUser

class Clientes(models.Model):
    nickname = models.CharField("Código", max_length=100, blank=True, null=True)
    nome = models.CharField("Nome", max_length=100, blank=True, null=True)
    sexo = models.CharField("Sexo", max_length=100, blank=True, null=True)
    email = models.CharField("Telefone", max_length=100, blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=100, blank=True, null=True)
    assessor = models.CharField("Assessor", max_length=100, blank=True, null=True)
    antigo_assessor = models.CharField("Antigo Assessor", max_length=100, blank=True, null=True)
    data_nascimento =models.CharField("Nascimento", max_length=100, blank=True, null=True)

    d0 = models.CharField("Saldo em D0", max_length=100, blank=True, null=True)
    d1 = models.CharField("Saldo em D1", max_length=100, blank=True, null=True)
    d2 = models.CharField("Saldo em D2", max_length=100, blank=True, null=True)
    d3 = models.CharField("Saldo em D3", max_length=100, blank=True, null=True)
    d4 = models.CharField("Saldo em D4", max_length=100, blank=True, null=True)

    status = models.CharField("Status", max_length=100, blank=True, null=True)
    troca = models.CharField("Troca", max_length=100, blank=True, null=True)
    rotina = models.BooleanField(default=False)
    cliente_dia = models.BooleanField(default=False)
    data_registro = models.DateTimeField(auto_now_add=True, blank=True)
    last_update = models.DateTimeField(auto_now=True, blank=True, null=True)
    token = models.TextField(blank=True, null=True)

class ClientsOnbording(models.Model):
    choiceFreqContato = (("Não Definido", "Não Definido"),("1 mes", "1 mes"),("3 meses", "3 meses"),("6 meses", "6 meses"),("12 meses", "12 meses"))
    choiceAcompanPerm = (("Não Definido", "Não Definido"),("WhatsApp", "WhatsApp"),("Telefone", "Telefone"),("Email", "Email"))

    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    assessor = models.CharField("Assessor", max_length=100, blank=True, null=True)

    email = models.BooleanField(default=False, blank=True, null=True)
    frequencia_contato = models.CharField(max_length=12, choices=choiceFreqContato, blank=True, null=True)
    perfil_preenchido = models.DateTimeField(blank=True, null=True)
    meio_contato = models.CharField(max_length=12, choices=choiceAcompanPerm, blank=True, null=True)
    acomp_permanente = models.BooleanField(default=False, blank=True, null=True)

    oportunidade_rf = models.BooleanField(default=False, blank=True, null=True)
    oportunidade_acoes = models.BooleanField(default=False, blank=True, null=True)
    oportunidade_fii = models.BooleanField(default=False, blank=True, null=True)
    oportunidade_fundos = models.BooleanField(default=False, blank=True, null=True)

    sujestao = models.DateTimeField(blank=True, null=True)
    alocacao = models.DateTimeField(blank=True, null=True)

    obs = models.TextField(blank=True, null=True)

class Espelhamento(models.Model):
    assessor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assessor_permited = models.IntegerField('Assessor a Espelhar')
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.assessor.first_name)

class NovoEmail(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    id_email = models.IntegerField(blank=False, null=False)
    categ_email_id = models.IntegerField(blank=False, null=False)
    data_futuro = models.DateField(blank=False, null=False)
    status = models.CharField(max_length=100, blank=True, null=True)
    data_status = models.DateField(blank=True, null=True)
    manual = models.CharField(max_length=100, blank=True, null=True)
    data_manual = models.DateField(blank=True, null=True)


class RegistroAtividades(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    registro = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    assessor_responsavel = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)



