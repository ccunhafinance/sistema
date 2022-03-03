from django.db import models

# categoria
class Categoria(models.Model):
    nome = models.CharField("Nome", max_length=255, null=False, blank=False)
    criado_por = models.IntegerField('Criado por:', null=False, blank=False)
    editado_por = models.IntegerField('Editado por:', null=False, blank=False)
    data_insert = models.CharField('Data de cadastro',max_length=255, null=False, blank=False)
    data_edited = models.CharField('Data de edição',max_length=255, null=True, blank=True)

# emails
class EmailCategoria(models.Model):
    EmailCategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField('Nome',max_length=255, null=False, blank=False)
    body = models.TextField("Body", null=True, blank=True)
    criado_por = models.IntegerField('Criado por:', null=True, blank=True)
    editado_por = models.IntegerField('Editado por:', null=True, blank=True)
    data_insert = models.CharField('Data de cadastro', max_length=255, null=True, blank=True)
    data_edited = models.CharField('Data de edição', max_length=255, null=True, blank=True)


