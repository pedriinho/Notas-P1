# Generated by Django 4.2 on 2023-06-13 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_classroom_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='StateThread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(default='deactive', max_length=20)),
            ],
        ),
    ]
