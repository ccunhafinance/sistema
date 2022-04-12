# Generated by Django 3.2.6 on 2022-04-12 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_clientes_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='nome_completo',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome Completo'),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='antigo_assessor',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Antigo Assessor'),
        ),
    ]
