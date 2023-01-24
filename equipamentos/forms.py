from django import forms
from django.forms import *
from .models import *
from django.forms import modelform_factory
from django.forms import BaseModelFormSet

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
        def clean(self):
            super().clean()
class  localFormlista(ModelForm):
    ListaLocais = modelformset_factory(Local_instalacao, fields=('__all__'))
    class Meta:
        model = Local_instalacao
        fields = '__all__'
    def clean(self):
            super().clean() 

class equipamentoEditarForm(ModelForm):
    class Meta:
        model=Equipamento
        fields=['nome_equipamento','nome_equipamento','fabricante','local','tipo_equipamento','data_compra','data_ultima_calibracao',
        'patrimonio','material_consumo']
        widgets = {
        'nome_equipamento': TextInput (attrs={'class': "form-control"}),
        'nome_equipamento':TextInput (attrs={'class': "form-control"}),
        'fabricante':Select (attrs={'class': "form-control"}),
        'local':Select (attrs={'class': "form-control"}),
        'tipo_equipamento':Select (attrs={'class': "form-control"}),
        'data_compra':SelectDateWidget (attrs={'class': "form-control"}),
        'data_ultima_calibracao':SelectDateWidget (attrs={'class': "form-control"}),
        'patrimonio':TextInput (attrs={'class': "form-control"}),
        'material_consumo':CheckboxSelectMultiple (attrs={'class': "form-control"}),
    }
    def clean(self):
            super().clean()

class equipamentoCadastrarForm(ModelForm):
    class Meta:
        model=Equipamento
        fields=['nome_equipamento','modelo','fabricante','local','tipo_equipamento','data_compra','data_ultima_calibracao',
        'patrimonio','material_consumo']
        widgets = {
        'nome_equipamento': TextInput (attrs={'class': "form-control"}),
        'modelo':TextInput (attrs={'class': "form-control"}),
        'fabricante':Select (attrs={'class': "form-control"}),
        'local':Select (attrs={'class': "form-control"}),
        'tipo_equipamento':Select (attrs={'class': "form-control"}),
        'data_compra':SelectDateWidget (attrs={'class': "form-control"}),
        'data_ultima_calibracao':SelectDateWidget (attrs={'class': "form-control"}),
        'patrimonio':TextInput (attrs={'class': "form-control"}),
        'material_consumo':SelectMultiple (attrs={'class': "form-control"}),
        
    }
    def clean(self):
        super().clean()
        print(self.cleaned_data['tipo_equipamento'])
        
        numero=len(Equipamento.objects.filter(tipo_equipamento=self.fields['tipo_equipamento'].id))
        
        self.fields['codigo']=self.fields['tipo_equipamento'][:3]+numero
    

    
   

