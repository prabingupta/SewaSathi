from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['preferred_date', 'preferred_time_slot', 'address', 'notes']
        widgets = {
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

    def clean_preferred_date(self):
        from django.utils import timezone
        date = self.cleaned_data['preferred_date']
        if date < timezone.now().date():
            raise forms.ValidationError("You can't book a date in the past.")
        return date
