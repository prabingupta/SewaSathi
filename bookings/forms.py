from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'preferred_date', 'preferred_time_slot', 'address', 'notes']
        widgets = {
            'service': forms.Select(attrs={'class': 'ss-form-control'}),
            'preferred_date': forms.DateInput(attrs={'class': 'ss-form-control', 'type': 'date'}),
            'preferred_time_slot': forms.Select(attrs={'class': 'ss-form-control'}),
            'address': forms.TextInput(attrs={
                'class': 'ss-form-control',
                'placeholder': 'Where should the provider come?'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'ss-form-control', 'rows': 3,
                'placeholder': 'Describe what you need help with...'
            }),
        }

    def __init__(self, *args, provider=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].required = False
        self.fields['service'].empty_label = "General inquiry (no specific service)"
        if provider:
            self.fields['service'].queryset = provider.services.filter(is_active=True)

    def clean_preferred_date(self):
        from django.utils import timezone
        date = self.cleaned_data['preferred_date']
        if date < timezone.now().date():
            raise forms.ValidationError("You can't book a date in the past.")
        return date
