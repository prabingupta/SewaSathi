from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(5, '5 - Excellent'), (4, '4 - Good'), (3, '3 - Average'), (2, '2 - Poor'), (1, '1 - Terrible')],
        widget=forms.Select(attrs={'class': 'ss-form-control'})
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'ss-form-control', 'rows': 4,
                'placeholder': 'How was your experience?'
            }),
        }
