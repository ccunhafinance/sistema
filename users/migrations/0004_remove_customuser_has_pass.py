# Generated by Django 3.2.5 on 2021-08-18 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_has_pass'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='has_pass',
        ),
    ]
