# remitos/forms.py
from django import forms
from .models import Remito

class RemitoForm(forms.ModelForm):
    class Meta:
        model = Remito
        fields = ['empresa', 'fecha_inicio', 'fecha_fin', 'importe_total']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'importe_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'empresa': forms.Select(attrs={'class': 'form-control'}),
        }
