# Generated by Django 4.1.5 on 2023-02-03 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0002_usuario_primeiro_acesso'),
        ('equipamentos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disciplina', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Modo_Falha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modo_falha', models.CharField(max_length=50)),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='notas.disciplina')),
            ],
        ),
        migrations.CreateModel(
            name='Modo_falha_equipamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipamento', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='equipamentos.equipamento')),
                ('modo_falha', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='notas.modo_falha')),
            ],
        ),
        migrations.CreateModel(
            name='Nota_material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.DecimalField(decimal_places=2, max_digits=12)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='equipamentos.material_consumo')),
            ],
        ),
        migrations.CreateModel(
            name='Nota_equipamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('descricao', models.TextField()),
                ('data_cadastro', models.DateTimeField(auto_now=True)),
                ('data_ocorrencia', models.DateField()),
                ('falha', models.BooleanField()),
                ('calibracao', models.BooleanField()),
                ('lubrificao', models.BooleanField()),
                ('equipamento', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='equipamentos.equipamento')),
                ('material', models.ManyToManyField(blank=True, to='notas.nota_material')),
                ('modo_Falha_equipamento', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='notas.modo_falha_equipamento')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuarios.usuario')),
            ],
        ),
    ]
