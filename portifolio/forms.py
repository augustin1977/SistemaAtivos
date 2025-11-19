from django.forms import *
from .models import *
from usuarios.models import *
from django.db.models import Q
from .codigo_barras import gerar_codigo_limpo

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
        if nome:
            nome = nome.strip().capitalize()
            cd["nome"] = nome
        if tonalidade:
            tonalidade = tonalidade.strip().upper()
            cd["tonalidade"] = tonalidade
        
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
    


class EtiquetaForm(Form):

    id = CharField(widget=HiddenInput(), required=False)

    projeto = ModelChoiceField(
        queryset=Projeto.objects.filter(ativo=True),
        widget=Select(attrs={"class": "form-control"}),
        required=True,
        label="Projeto"
    )

    amostra = ModelChoiceField(
        queryset=Amostra.objects.none(),
        widget=Select(attrs={'class': 'form-control'}),
        required=True,
        label="Amostra"
    )

    local_instalacao = ModelChoiceField(
        queryset=Local_instalacao.objects.all(),
        widget=Select(attrs={'class': 'form-control'})
    )

    massa = DecimalField(
        max_digits=10,
        decimal_places=3,
        required=False,
        label="Massa (kg)",
        widget=NumberInput(attrs={'class': 'form-control'})
    )

    observacao = CharField(
        required=False,
        widget=Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # SE FOR POST (CADASTRO OU EDIÇÃO)
        if self.data and self.data.get("projeto"):
            projeto_id = self.data.get("projeto")
            self.fields["amostra"].queryset = Amostra.objects.filter(
                projeto_id=projeto_id,
                data_fim__isnull=True
            )
            return  # <-- importantíssimo, evita sobrescrever depois

        # SE FOR EDIÇÃO (GET)
        initial = kwargs.get("initial")
        if initial:
            amostra = initial.get("amostra")
            if amostra:
                projeto = amostra.projeto
                self.fields["projeto"].initial = projeto
                self.fields["amostra"].queryset = Amostra.objects.filter(
                    projeto=projeto, data_fim__isnull=True
                )

    def clean(self):
        cd = super().clean()

        projeto = cd.get("projeto")
        amostra = cd.get("amostra")

        if not projeto:
            self.add_error("projeto", "Selecione um projeto.")

        if not amostra:
            self.add_error("amostra", "Selecione uma amostra.")

        # Se tiver erro, nem gera código
        if self.errors:
            return cd

        # Geração automática
        projeto = amostra.projeto

        ultimo = Etiqueta.objects.filter(amostra__projeto=projeto).order_by("-id").first()
        sequencia = 1 if not ultimo else int(ultimo.codigo_humano.split("-")[-1]) + 1

        cd["codigo_humano"] = (
            f"{gerar_codigo_limpo(projeto.nome)}-"
            f"{gerar_codigo_limpo(amostra.nome)}-"
            f"{sequencia:04d}"
        )

        ultimo_num = Etiqueta.objects.order_by("-id").first()
        cd["codigo_numerico"] = f"{(ultimo_num.id + 1) if ultimo_num else 1:09d}"

        cd["massa"] = cd.get("massa") or 0

        return cd
