# Generated by Django 3.2.6 on 2022-02-07 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_remove_clientes_d5'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='status',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Status'),
        ),
    ]
