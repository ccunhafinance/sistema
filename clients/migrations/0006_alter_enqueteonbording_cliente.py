# Generated by Django 3.2.6 on 2022-04-23 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_enqueteonbording'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enqueteonbording',
            name='cliente',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Código do Cleiente'),
        ),
    ]
