# Generated by Django 4.1.5 on 2023-02-16 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0007_alter_media_documentos'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='data_cadastro',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
