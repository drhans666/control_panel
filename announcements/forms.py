from django import forms
from .models import Anon



class AnonForm(forms.ModelForm):
    class Meta:
        model = Anon
        fields = ['title', 'text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}