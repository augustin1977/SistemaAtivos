from django import forms
from django.forms import *
from .models import *
from django.forms import modelform_factory
from django.forms import BaseModelFormSet
import datetime

class localFormCadastro(ModelForm):
    class Meta:
        model = Local_instalacao
        fields = '__all__'
        widgets = {
            'predio': TextInput (attrs={'class': "form-control"}),
            'piso':TextInput (attrs={'class': "form-control"}),
            'sala':TextInput (attrs={'class': "form-control"}),
            'armario':TextInput (attrs={'class': "form-control"}),
            'prateleira':TextInput (attrs={'class': "form-control"}),
            'apelido_local':TextInput (attrs={'class': "form-control"}),

        }
class  localFormlista(ModelForm):
    ListaLocais = modelformset_factory(Local_instalacao, fields=('__all__'))
    class Meta:
        model = Local_instalacao
        fields = '__all__'


class equipamentoEditarForm(ModelForm):
   

    class Meta:
        model=Equipamento
        anoAtual=datetime.datetime.now().year
        fields=['nome_equipamento','fabricante','local','tipo_equipamento','data_compra','data_ultima_calibracao',
        'patrimonio','material_consumo']
        widgets = {
        'nome_equipamento':TextInput (attrs={'class': "form-control"}),
        'fabricante':Select (attrs={'class': "form-control"}),
        'local':Select (attrs={'class': "form-control"}),
        'tipo_equipamento':Select (attrs={'class': "form-control"}),
        'data_compra':SelectDateWidget (attrs={'class': "form-control"}),
        'data_ultima_calibracao':SelectDateWidget (attrs={'class': "form-control"}),
        'patrimonio':TextInput (attrs={'class': "form-control"}),
        'material_consumo':CheckboxSelectMultiple (attrs={'class': "form-control"}),
    }


class equipamentoCadastrarForm(ModelForm):
    nome_equipamento=TextInput()
    fabricante=Select()
    local=Select()
    Tipo_equipamento=Select()
    
    class Meta:
        model=Equipamento
        anoAtual=datetime.datetime.now().year
        fields=['nome_equipamento','modelo','fabricante','local','tipo_equipamento','data_compra','data_ultima_calibracao',
        'patrimonio','material_consumo','usuario']
        
        widgets = {
        'usuario': HiddenInput(attrs={'class': "form-control"}),
        'nome_equipamento': TextInput (attrs={'class': "form-control"}),
        'modelo':TextInput (attrs={'class': "form-control"}),
        'fabricante':Select (attrs={'class': "form-control"}),
        'local':Select (attrs={'class': "form-control"}),
        'tipo_equipamento':Select (attrs={'class': "form-control"}),
        'data_compra':SelectDateWidget (years=tuple(range(1900,anoAtual+1)),attrs={'class': "form-control"}),
        'data_ultima_calibracao':SelectDateWidget (years=tuple(range(1900,anoAtual+1)),attrs={'class': "form-control"}),
        'patrimonio':TextInput (attrs={'class': "form-control"}),
        'material_consumo':SelectMultiple (attrs={'class': "form-control"}),
        
    }
    
    

    
   

