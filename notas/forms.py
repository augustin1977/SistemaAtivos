from django import forms
from django.forms import *
from .models import *
from django.forms import modelform_factory
from django.forms import BaseModelFormSet
from cadastro_equipamentos.settings import TIME_ZONE
from equipamentos.models import *
import datetime
import pytz

class Disciplina(models.Model):

     class Meta:
        model = Disciplina
        fields = '__all__'
        widgets = {
            'disciplina': TextInput (attrs={'class': "form-control"}),
            }
class Modo_Falha (models.Model):
    model = Modo_Falha
    fields = '__all__'
    widgets = {
        'disciplina': Select (attrs={'class': "form-control"}),
        'modo_falha':TextInput (attrs={'class': "form-control"})
        }
    
class Modo_falha_equipamento (models.Model):
    model = Modo_falha_equipamento
    fields = '__all__'
    widgets = {
        'modo_falha': Select (attrs={'class': "form-control"}),
        'equipamento':Select (attrs={'class': "form-control"})
        }
class Nota_material (models.Model):
    model = Nota_material
    fields = '__all__'
    widgets = {
        'material': Select (attrs={'class': "form-control"}),
        'quantidade':DecimalField (attrs={'class': "form-control"})
        }
    
class Nota_equipamento (models.Model):
    model = Nota_equipamento
    fields = '__all__'
    widgets = {
        'titulo': TextInput (attrs={'class': "form-control"}),
        'descricao':Textarea (attrs={'class': "form-control"}),
        'equipamento':Select (attrs={'class': "form-control"}),
        'modo_Falha_equipamento':Select (attrs={'class': "form-control"}),
        'material':Select (attrs={'class': "form-control"}),
        'data_ocorrencia':DateTimeField (attrs={'class': "form-control"}),
        'falha': CheckboxInput (attrs={'class': "form-control"}),
        'calibracao':CheckboxInput (attrs={'class': "form-control"}),
        'lubrificao':CheckboxInput (attrs={'class': "form-control"}),
        }
    def clean(self):
        super().clean()
        cd=self.cleaned_data
        utc=pytz.timezone(TIME_ZONE)
        cd['data_cadastro']=utc.localize( datetime.datetime.now())
        if (cd['calibracao']):
               equipamento=Equipamento.objects.get(cd['equipamento'])
               equipamento.data_ultima_calibracao=utc.localize( datetime.datetime.now())
               equipamento.save()


    