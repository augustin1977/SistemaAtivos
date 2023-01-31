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
class localFormEditar(ModelForm):
    id=CharField(label="",widget=HiddenInput())
    class Meta:
        model = Local_instalacao
        fields = '__all__'
        widgets = {
            'id': HiddenInput(),
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


class equipamentoEditarForm(Form):
    id=CharField(label="",widget=HiddenInput())
    nome_equipamento=CharField(widget= TextInput(attrs={'class': "form-control"}))
    modelo=CharField(widget= TextInput(attrs={'class': "form-control"}))
    fabricante=ModelChoiceField(queryset=Fabricante.objects.all() ,widget=Select (attrs={'class': "form-control"}))
    local=ModelChoiceField(queryset=Local_instalacao.objects.all(),widget=Select(attrs={'class': "form-control"}))
    tipo_equipamento=ModelChoiceField(queryset= Tipo_equipamento.objects.all(),widget=Select(attrs={'class': "form-control"}))
    anoAtual=datetime.datetime.now().year
    data_compra=DateTimeField(widget=SelectDateWidget(years=tuple(range(1900,anoAtual+1)),attrs={'class': "form-control"}))
    data_ultima_calibracao=DateTimeField(widget=SelectDateWidget(years=tuple(range(1900,anoAtual+1)),attrs={'class': "form-control"}))
    patrimonio=CharField(widget= TextInput(attrs={'class': "form-control"}))
    material_consumo=ModelMultipleChoiceField(required=False,blank=True,queryset= Material_consumo.objects.all(),widget=SelectMultiple(attrs={'class': "form-control"}))
    usuario=CharField(label="",widget=HiddenInput())

    
    def clean(self):
        super().clean()
        utc=pytz.UTC
        cd=self.cleaned_data
        cd['data_cadastro']=utc.localize( datetime.datetime.now())
        data_compra=cd["data_compra"]
        data_cadastro=cd["data_cadastro"]
        if data_compra>data_cadastro:
            raise ValidationError('Data Compra invalida: a data de compra deve ser anterior a data de hoje')
        tipo_equipamento=cd["tipo_equipamento"]
        tipo=Tipo_equipamento.objects.get(id=tipo_equipamento.id)
        numero=len(Equipamento.objects.filter(tipo_equipamento=tipo_equipamento.id))+1
        cd['codigo']=f'{tipo.sigla.upper()}{numero:03d}'
        return cd


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
    material_consumo=ModelMultipleChoiceField(required=False,blank=True,queryset= Material_consumo.objects.all(),widget=SelectMultiple(attrs={'class': "form-control"}))
    usuario=CharField(label="",widget=HiddenInput())

    
    def clean(self):
        super().clean()
        utc=pytz.UTC
        cd=self.cleaned_data
        cd['data_cadastro']=utc.localize( datetime.datetime.now())
        data_compra=cd["data_compra"]
        data_cadastro=cd["data_cadastro"]
        if data_compra>data_cadastro:
            raise ValidationError('Data Compra invalida: a data de compra deve ser anterior a data de hoje')
        tipo_equipamento=cd["tipo_equipamento"]
        tipo=Tipo_equipamento.objects.get(id=tipo_equipamento.id)
        numero=len(Equipamento.objects.filter(tipo_equipamento=tipo_equipamento.id))+1
        cd['codigo']=f'{tipo.sigla.upper()}{numero:03d}'
        return cd

    
class cadastraTipo_equipamento(Form):
    nome=CharField(widget= TextInput(attrs={'class': "form-control"}))
    descricao=CharField(widget=Textarea(attrs={'class': "form-control"}))
    sigla=CharField(label="",widget=HiddenInput())
    def descricao_clean(self):
        cd=self.cleaned_data
        return cd

    def clean(self):
        super().clean()
        cd=self.cleaned_data
        siglas=[]
        tipos=Tipo_equipamento.objects.all()
        for tipo in tipos:
            siglas.append(tipo.sigla)
        cd['sigla']=cd['nome'][0:3]
        i=3
        while(cd['sigla'] in siglas  and i<len(cd['nome'])):
            cd['siglas']=cd['nome'][0:2]+cd['nome'][i]
        if i>len(cd['nome']):
            cd['siglas']=cd['nome'][0:2]+'x'
        return cd
