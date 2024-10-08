from django import forms
from django.forms import *
from .models import *
from django.forms import modelform_factory
from django.forms import BaseModelFormSet
from cadastro_equipamentos.settings import TIME_ZONE
from equipamentos.models import *
import datetime
import pytz

class cadastraDisciplinaForm(ModelForm):
     class Meta:
        model = Disciplina
        fields = '__all__'
        widgets = {
            'disciplina': TextInput (attrs={'class': "form-control"}),
            }
class CadastraModo_FalhaForm (ModelForm):
   class Meta:
        model = Modo_Falha
        fields = '__all__'
        widgets = {
            'disciplina': Select (attrs={'class': "form-control"}),
            'modo_falha':TextInput (attrs={'class': "form-control"})
            }
        
class CadastraModo_falha_equipamentoForm (ModelForm):
    equipamento = ModelChoiceField(queryset=Equipamento.objects.filter(ativo=True),widget=Select(attrs={'class': "form-control"}))
    class Meta:
        model = Modo_falha_equipamento
        
        fields = ['equipamento','modo_falha']
        widgets = {
            'modo_falha': Select (attrs={'class': "form-control"}),
            
            }
        
        
# class CadastraNota_materialForm (ModelForm):
#     class Meta:
#         model = Nota_material
#         fields = '__all__'
#         widgets = {
#             'material': Select (attrs={'class': "form-control"}),
#             'quantidade':NumberInput (attrs={'class': "form-control"})
#             }
    
class CadastraNota_equipamentoForm(ModelForm):
    equipamento = ModelChoiceField(
        queryset=Equipamento.objects.filter(ativo=True),
        widget=Select(attrs={'class': 'form-control'})
    )
    modo_Falha_equipamento = ModelChoiceField(
        queryset=Modo_falha_equipamento.objects.none(),
        widget=Select(attrs={'class': 'form-control'})
    )
    """material=ModelMultipleChoiceField(
        queryset=Material_consumo.objects.all(),
        widget=SelectMultiple(attrs={'class': 'form-control'})
        )"""

    class Meta:
        model = Nota_equipamento
        fields = ['titulo', 'descricao', 'equipamento', 'modo_Falha_equipamento',  'data_ocorrencia', 'melhoria','falha', 'calibracao', 'lubrificao']
        widgets = {
            'titulo': TextInput(attrs={'class': 'form-control','placeholder':'Nome da ocorrencia para futura referencia e pesquisa'}),
            'descricao': Textarea(attrs={'class': 'form-control','placeholder':'Descrição detalhada da ocorrencia'}),
            'data_ocorrencia': DateInput(attrs={'class': 'form-control','placeholder':'Data da ocorrencia no formato dd/mm/aaaa'}),
            'falha': CheckboxInput(attrs={'class': 'form-control'}),
            'calibracao': CheckboxInput(attrs={'class': 'form-control'}),
            'lubrificao': CheckboxInput(attrs={'class': 'form-control'}),
            'melhoria': CheckboxInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'equipamento' in self.data:
            equipamento_id = int(self.data.get('equipamento'))
            self.fields['modo_Falha_equipamento'].queryset = Modo_falha_equipamento.objects.filter(equipamento_id=equipamento_id)
        elif self.instance.pk:
            self.fields['modo_Falha_equipamento'].queryset = self.instance.equipamento.modo_falha_equipamento_set.all()

    def clean(self):
        super().clean()
        cd=self.cleaned_data
        utc=pytz.timezone(TIME_ZONE)
        cd['data_cadastro']=utc.localize( datetime.datetime.now())
        if (cd['calibracao'] or cd['melhoria']):
               #print('equipamento',cd['equipamento'])
               equipamento=Equipamento.objects.get(id=cd['equipamento'].id)
               equipamento.data_ultima_calibracao=utc.localize( datetime.datetime.now())
               equipamento.save()   

class exibirDetalheNotaForm(ModelForm):
   class Meta:
        model = Nota_equipamento
        fields = "__all__"
        widgets = {
            'titulo': TextInput(attrs={'class': 'form-control'}),
            'descricao': Textarea(attrs={'class': 'form-control'}),
            'equipamento':TextInput(attrs={'class': 'form-control'}),
            'material': TextInput(attrs={'class': 'form-control'}),
            'modo_Falha_equipamento': TextInput(attrs={'class': 'form-control'}),
            'data_ocorrencia': DateInput(attrs={'class': 'form-control'}),
            'falha': CheckboxInput(attrs={'class': 'form-control'}),
            'calibracao': CheckboxInput(attrs={'class': 'form-control'}),
            'lubrificao': CheckboxInput(attrs={'class': 'form-control'}),
            'melhoria': CheckboxInput(attrs={'class': 'form-control'}),}
        




