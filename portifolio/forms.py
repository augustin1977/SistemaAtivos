from django.forms import *
from .models import *
from usuarios.models import *
from django.db.models import Q
from django.utils.text import slugify

class CorForm(Form):
    id = CharField(label="", required=False, widget=HiddenInput())
    nome = CharField(widget=TextInput(attrs={'class': "form-control"}))
    tonalidade = CharField(widget=TextInput(attrs={'class': "form-control", 'placeholder': "#RRGGBB"}))
    #ativa = BooleanField(required=False, label="Ativa")

    def clean(self):
        super().clean()
        cd = self.cleaned_data
        
        nome = cd.get("nome")
        tonalidade = cd.get("tonalidade")
        id_val = cd.get("id") or None  # evita string vazia

        # validação de nome duplicado
        qs = Cor.objects.filter(nome__iexact=nome)
        if id_val:
            qs = qs.exclude(id=id_val)
        if nome and qs.exists():
            self.add_error("nome", "Já existe uma cor com esse nome.")

        # validação de tonalidade duplicada
        qs = Cor.objects.filter(tonalidade__iexact=tonalidade)
        if id_val:
            qs = qs.exclude(id=id_val)
        if tonalidade and qs.exists():
            self.add_error("tonalidade", "Essa tonalidade já está cadastrada.")

        return cd


class ProjetoForm(Form):
    id = CharField(label="", widget=HiddenInput(), required=False)
    nome = CharField(widget=TextInput(attrs={'class': "form-control"}))
    cliente = CharField(widget=TextInput(attrs={'class': "form-control"}))

    # 🔹 só mostra cores inativas
    cor = ModelChoiceField(
        queryset=Cor.objects.filter(ativa=False),
        widget=Select(attrs={'class': 'form-control'}),
        empty_label="Selecione uma cor inativa",
        required=True
    )

    responsavel = ModelChoiceField(
        queryset=Usuario.objects.filter(ativo=True),
        widget=Select(attrs={'class': 'form-control'}),
        empty_label="Selecione o responsável",
        required=True
    )

    #ativo = BooleanField(required=False, label="Ativo", initial=True)
    def __init__(self, *args, **kwargs):
        cor_atual = kwargs.pop("cor_atual", None)  # passe a cor do projeto ao editar
        super().__init__(*args, **kwargs)
        if cor_atual is not None:
            self.fields["cor"].queryset = Cor.objects.filter(Q(ativa=False) | Q(pk=cor_atual.pk))
        else:
            self.fields["cor"].queryset = Cor.objects.filter(ativa=False)

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get("nome")
        id_atual = cleaned_data.get("id")

        if nome:
            # 🔍 Ignora o próprio registro ao editar
            projetos = Projeto.objects.filter(nome__iexact=nome)
            if id_atual:
                projetos = projetos.exclude(id=id_atual)
            if projetos.exists():
                raise forms.ValidationError("Já existe um projeto com este nome.")

        return cleaned_data
    

class AmostraForm(Form):
    id = CharField(label="", widget=HiddenInput(), required=False)
    nome = CharField(label="Nome da Amostra", widget=TextInput(attrs={'class': 'form-control'}))
    projeto = ModelChoiceField(
        queryset=Projeto.objects.filter(ativo=True).order_by('nome'),
        label="Projeto",
        widget=Select(attrs={'class': 'form-control'})
    )
    data_recebimento = DateField(
        label="Data de Recebimento",
        widget=DateInput(attrs={'class': 'form-control', 'type': 'date'},format='%Y-%m-%d'),input_formats=['%Y-%m-%d']
    )
    prazo_dias = IntegerField(
        label="Prazo (dias)",
        widget=NumberInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cd = super().clean()
        nome = cd.get("nome")
        projeto = cd.get("projeto")
        if nome and projeto:
            amostras = Amostra.objects.filter(nome__iexact=nome, projeto=projeto)
            if cd.get("id"):
                amostras = amostras.exclude(id=cd.get("id"))
            if amostras.exists():
                raise forms.ValidationError("Já existe uma amostra com este nome neste projeto.")
        return cd
    


class EtiquetaForm(forms.Form):
    id = CharField(widget=HiddenInput(), required=False)
    amostra = ModelChoiceField(
        queryset=Amostra.objects.filter(projeto__ativo=True, data_fim__isnull=True),
        widget=Select(attrs={'class': 'form-control'})
    )
    local_instalacao = ModelChoiceField(
        queryset=Local_instalacao.objects.all(),
        widget=Select(attrs={'class': 'form-control'})
    )
    massa = DecimalField(
        max_digits=10,
        decimal_places=3,
        widget=NumberInput(attrs={'class': 'form-control'})
    )
    quantidade = IntegerField(
        min_value=1,
        max_value=1000,
        initial=1,
        label="Número de etiquetas a gerar",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    observacao = CharField(
        required=False,
        widget=Textarea(attrs={'class': 'form-control'})
    )

    def clean(self):
        cd = super().clean()
        amostra = cd.get("amostra")

        # Geração automática do código humano e numérico
        if amostra:
            projeto = amostra.projeto
            prefixo_projeto = slugify(projeto.nome)[:4].upper()
            prefixo_amostra = slugify(amostra.nome)[:3].upper()

            ultimo = Etiqueta.objects.filter(amostra__projeto=projeto).order_by('-id').first()
            sequencia = 1 if not ultimo else int(ultimo.codigo_humano.split('-')[-1]) + 1
            cd['codigo_humano'] = f"{prefixo_projeto}-{prefixo_amostra}-{sequencia:05d}"

            ultimo_num = Etiqueta.objects.order_by('-id').first()
            cd['codigo_numerico'] = f"{(ultimo_num.id + 1) if ultimo_num else 1:09d}"

        return cd
