# Generated by Django 4.1.5 on 2023-02-16 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0005_alter_equipamento_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='media',
        ),
    ]
