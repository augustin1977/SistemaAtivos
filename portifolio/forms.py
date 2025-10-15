from django.forms import *
from .models import *
from usuarios.models import *
from django.db.models import Q

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


class ProjetoForm(forms.Form):
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