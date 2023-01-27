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


class equipamentoCadastrarForm(Form):
    nome_equipamento=CharField(widget= TextInput(attrs={'class': "form-control"}))
    modelo=CharField(widget= TextInput(attrs={'class': "form-control"}))
    fabricante=ModelChoiceField(queryset=Fabricante.objects.all() ,widget=Select (attrs={'class': "form-control"}))
    local=ModelChoiceField(queryset=Local_instalacao.objects.all(),widget=Select(attrs={'class': "form-control"}))
    tipo_equipamento=ModelChoiceField(queryset= Tipo_equipamento.objects.all(),widget=Select(attrs={'class': "form-control"}))
    anoAtual=datetime.datetime.now().year
    data_compra=DateTimeField(widget=SelectDateWidget(years=tuple(range(1900,anoAtual+1)),attrs={'class': "form-control"}))
    data_ultima_calibracao=DateTimeField(widget=SelectDateWidget(years=tuple(range(1900,anoAtual+1)),attrs={'class': "form-control"}))
    patrimonio=CharField(widget= TextInput(attrs={'class': "form-control"}))
    material_consumo=ModelMultipleChoiceField(queryset= Material_consumo.objects.all(),widget=SelectMultiple(attrs={'class': "form-control"}))
    usuario=CharField(label="",widget=HiddenInput())

    
    def clean(self):
        super().clean()
        utc=pytz.UTC
        cd=self.cleaned_data
        print(cd)
        cd['data_cadastro']=utc.localize( datetime.datetime.now())
        data_compra=cd["data_compra"]
        data_cadastro=cd["data_cadastro"]
        if data_compra>data_cadastro:
            print(KeyError)
            raise ValidationError('Data Compra invalida: a data de compra deve ser anterior a data de hoje')
        tipo_equipamento=cd["tipo_equipamento"]
        tipo=Tipo_equipamento.objects.get(id=tipo_equipamento.id)
        numero=len(Equipamento.objects.filter(tipo_equipamento=tipo_equipamento.id))+1
        cd['codigo']=f'{tipo.sigla.upper()}{numero:03d}'
        return cd



    
    

    
   

