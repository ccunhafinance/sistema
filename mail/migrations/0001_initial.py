# Generated by Django 3.2.6 on 2022-03-01 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('criado_por', models.IntegerField(verbose_name='Criado por:')),
                ('editado_por', models.IntegerField(verbose_name='Editado por:')),
                ('data_insert', models.CharField(max_length=255, verbose_name='Data de cadastro')),
                ('data_edited', models.CharField(blank=True, max_length=255, null=True, verbose_name='Data de edição')),
            ],
        ),
        migrations.CreateModel(
            name='EmailCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Body')),
                ('criado_por', models.IntegerField(verbose_name='Criado por:')),
                ('editado_por', models.IntegerField(verbose_name='Editado por:')),
                ('data_insert', models.CharField(max_length=255, verbose_name='Data de cadastro')),
                ('data_edited', models.CharField(blank=True, max_length=255, null=True, verbose_name='Data de edição')),
                ('EmailCategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mail.categoria')),
            ],
        ),
    ]
