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
    data_nascimento = models.CharField("Data de Nascimento", max_length=100, blank=True, null=True)
    d0 = models.CharField("Saldo em D0", max_length=100, blank=True, null=True)
    d1 = models.CharField("Saldo em D1", max_length=100, blank=True, null=True)
    d2 = models.CharField("Saldo em D2", max_length=100, blank=True, null=True)
    d3 = models.CharField("Saldo em D3", max_length=100, blank=True, null=True)
    d4 = models.CharField("Saldo em D4", max_length=100, blank=True, null=True)
    status = models.CharField("Status", max_length=100, blank=True, null=True)
    troca = models.CharField("Troca", max_length=100, blank=True, null=True)
    rotina = models.CharField("Rotina", max_length=100, blank=True, null=True)
    zap_mail = models.CharField("Zap", max_length=100, blank=True, null=True)
    cliente_dia = models.CharField("New", max_length=100, blank=True, null=True)
    data_registro = models.CharField("Data Registro", max_length=100, blank=True, null=True)
    # novos campos
    frequencia_contato = models.CharField(max_length=100, blank=True, null=True)
    onbording_acomp_per = models.CharField(max_length=100, blank=True, null=True)
    onbording_acomp_rf = models.CharField(max_length=100, blank=True, null=True)
    onbording_acomp_acoes = models.CharField(max_length=100, blank=True, null=True)
    onbording_acomp_fii = models.CharField(max_length=100, blank=True, null=True)
    onbording_acomp_fiinvest = models.CharField(max_length=100, blank=True, null=True)
    onbording_obs = models.TextField(blank=True, null=True)
    onbording_email = models.TextField(blank=True, null=True)
    onbording_envio_sugestao = models.TextField(blank=True, null=True)
    onbording_impl_envio_sugestao = models.TextField(blank=True, null=True)
    onbording_perfil_preenchido = models.TextField(blank=True, null=True)
    token = models.TextField(blank=True, null=True)



# Create your models here.
class Espelhamento(models.Model):
    assessor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assessor_permited = models.IntegerField('Assessor a Espelhar')
    data = models.DateField(default=date.today)

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



