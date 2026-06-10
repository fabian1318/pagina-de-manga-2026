from django import forms
from .models import Manga

class SubirCapituloForm(forms.Form):
    manga = forms.ModelChoiceField(
        queryset=Manga.objects.all(), 
        label="Selecciona el Manga", 
        widget=forms.Select(attrs={'class': 'form-select bg-dark text-light border-secondary'})
    )
    tomo = forms.DecimalField(
        max_digits=5, decimal_places=1, required=False, label="Tomo (Opcional)", 
        widget=forms.NumberInput(attrs={'class': 'form-control bg-dark text-light border-secondary'})
    )
    numero = forms.DecimalField(
        max_digits=5, decimal_places=1, label="Número del Capítulo", 
        widget=forms.NumberInput(attrs={'class': 'form-control bg-dark text-light border-secondary'})
    )
    titulo = forms.CharField(
        max_length=200, required=False, label="Título del Capítulo (Opcional)", 
        widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary'})
    )
    archivo = forms.FileField(
        label="Archivo del Capítulo (.cbz o .zip)", 
        widget=forms.FileInput(attrs={'class': 'form-control bg-dark text-light border-secondary'})
    )