# Generated by Django 3.2.6 on 2022-03-17 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='frequencia_contato',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientes',
            name='onbording_acomp_acoes',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientes',
            name='onbording_acomp_fii',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientes',
            name='onbording_acomp_fiinvest',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientes',
            name='onbording_acomp_per',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientes',
            name='onbording_acomp_rf',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientes',
            name='onbording_email',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clientes',
            name='onbording_envio_sugestao',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clientes',
            name='onbording_impl_envio_sugestao',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clientes',
            name='onbording_obs',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clientes',
            name='onbording_perfil_preenchido',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='RegistroAtividades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registro', models.CharField(blank=True, max_length=100, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('assessor_responsavel', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.clientes')),
            ],
        ),
    ]
