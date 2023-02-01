# Generated by Django 4.1.5 on 2023-02-01 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0011_alter_local_instalacao_options'),
        ('notas', '0005_alter_nota_equipamento_material'),
        ('log', '0002_log_movimento_alter_log_transacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='Nota_equipamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='notas.nota_equipamento'),
        ),
        migrations.AlterField(
            model_name='log',
            name='equipamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='equipamentos.equipamento'),
        ),
    ]
