# Generated by Django 3.2.5 on 2021-08-18 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='has_pass',
            field=models.BooleanField(default=False),
        ),
    ]
