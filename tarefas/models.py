from django.db import models
# Create your models here.

class RegitroVencimentoRF(models.Model):
  codigo_cliente = models.IntegerField(null=True, blank=True)
  status = models.CharField(max_length=200 ,default='...', blank=True, null=True)
  data = models.DateTimeField(auto_now_add=True)
