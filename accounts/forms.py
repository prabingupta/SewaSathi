from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.Role.choices,
        widget=forms.Select(attrs={'class': 'ss-form-control'}),
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ss-form-control', 'placeholder': 'e.g. 98XXXXXXXX'}),
    )
    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'ss-form-control', 'placeholder': 'City, area'}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'ss-form-control'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'phone', 'address', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'ss-form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'ss-form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'ss-form-control'})
