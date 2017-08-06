from django import forms
from .models import Item, ItemLocation


class ItemForm(forms.ModelForm):
    def clean_data(self):
        return self.cleaned_data['name', 'manufacturer'].capitalize()

    class Meta:
        model = Item
        fields = '__all__'


class ItemLocationForm(forms.ModelForm):
    class Meta:
        model = ItemLocation
        fields = ['item', 'quantity', 'section']
