# Generated by Django 4.1.5 on 2023-03-13 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0009_equipamento_ativo'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='local_instalacao',
            unique_together={('laboratorio', 'predio', 'piso', 'sala', 'armario', 'prateleira')},
        ),
    ]
