# Generated by Django 3.2.6 on 2022-02-18 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_rename_old_assessor_clientes_novo_assessor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientes',
            old_name='novo_assessor',
            new_name='antigo_assessor',
        ),
        migrations.AddField(
            model_name='clientes',
            name='data_registro',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Data Registro'),
        ),
        migrations.AddField(
            model_name='clientes',
            name='troca',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Troca'),
        ),
    ]