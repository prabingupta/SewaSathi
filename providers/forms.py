from django import forms
from .models import ServiceProvider


class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = [
            'category', 'bio', 'experience_years',
            'hourly_rate', 'service_area', 'citizenship_or_license'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'ss-form-control'}),
            'bio': forms.Textarea(attrs={
                'class': 'ss-form-control', 'rows': 4,
                'placeholder': 'Describe your skills, tools, and what makes you reliable...'
            }),
            'experience_years': forms.NumberInput(attrs={'class': 'ss-form-control', 'min': 0}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'ss-form-control', 'placeholder': 'e.g. 500'}),
            'service_area': forms.TextInput(attrs={'class': 'ss-form-control', 'placeholder': 'e.g. Kathmandu, Lalitpur'}),
            'citizenship_or_license': forms.FileInput(attrs={'class': 'ss-form-control'}),
        }
