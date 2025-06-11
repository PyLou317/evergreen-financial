from django import forms
from .models import *

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "date",
            "description",
            "category",
            "notes",
            "amount"
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }