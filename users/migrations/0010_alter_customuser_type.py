# Generated by Django 3.2.6 on 2022-05-25 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_userprofile_google_sheets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='type',
            field=models.CharField(choices=[('developer', 'Developer'), ('assessor', 'Assessor'), ('admin', 'Admin'), ('outros', 'Outros')], default='admin', max_length=50, verbose_name='Tipo de Usuário'),
        ),
    ]
