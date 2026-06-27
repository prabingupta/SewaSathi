from django import forms
from .models import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'ss-form-control', 'placeholder': 'e.g. Fan Installation'}),
            'description': forms.TextInput(attrs={'class': 'ss-form-control', 'placeholder': 'Optional short detail'}),
            'price': forms.NumberInput(attrs={'class': 'ss-form-control', 'placeholder': 'e.g. 300'}),
        }
