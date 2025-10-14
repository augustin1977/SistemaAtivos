from django.forms import *
from .models import *
from usuarios.models import *

class CorForm(Form):
    id = CharField(label="", required=False, widget=HiddenInput())
    nome = CharField(widget=TextInput(attrs={'class': "form-control"}))
    tonalidade = CharField(widget=TextInput(attrs={'class': "form-control", 'placeholder': "#RRGGBB"}))
    ativa = BooleanField(required=False, label="Ativa")

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

    ativo = BooleanField(required=False, label="Ativo", initial=True)

    def clean(self):
        super().clean()
        cd = self.cleaned_data
        nome = cd.get("nome")
        id_atual = cd.get("id") or None

        if nome:
            qs = Projeto.objects.filter(nome__iexact=nome)
            if id_atual:
                qs = qs.exclude(id=id_atual)
            if qs.exists():
                self.add_error("nome", "Já existe um projeto com esse nome.")
        return cd