# Generated by Django 2.2.19 on 2021-04-16 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplic', '0002_campeonato_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizador',
            name='cpf',
            field=models.CharField(max_length=11, unique=True, verbose_name='CPF'),
        ),
    ]