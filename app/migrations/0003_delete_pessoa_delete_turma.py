# Generated by Django 4.2.1 on 2023-06-01 01:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_pessoa'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Pessoa',
        ),
        migrations.DeleteModel(
            name='Turma',
        ),
    ]
