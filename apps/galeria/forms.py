from django import forms

from apps.galeria.models import Fotografia


class FotografiaForms(forms.ModelForm):
    class Meta:
        model = Fotografia
        exclude = ['publicada', 'usuario']
        labels = {
            'nome': 'Nome',
            'legenda': 'Legenda',
            'categoria': 'Categoria',
            'descricao': 'Descricao',
            'foto': 'Imagem',
            'data_fotografia': 'Data de registro',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Nebulosa de Orion'}),
            'legenda': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Capturada no observatorio'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descreva a fotografia'}
            ),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'data_fotografia': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                },
            ),
        }
