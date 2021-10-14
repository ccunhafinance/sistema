from datetime import date

from django.db import models
from users.models import CustomUser

# Create your models here.
class Espelhamento(models.Model):
    assessor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assessor_permited = models.IntegerField('Assessor a Espelhar')
    data = models.DateField(default=date.today)

    def __str__(self):
        return str(self.assessor.first_name)