# Generated by Django 3.2.6 on 2022-04-20 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_alter_clientes_last_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='nome',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome'),
        ),
    ]