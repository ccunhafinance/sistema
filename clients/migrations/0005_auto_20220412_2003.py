# Generated by Django 3.2.6 on 2022-04-12 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_auto_20220412_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='nome',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome'),
        ),
    ]
