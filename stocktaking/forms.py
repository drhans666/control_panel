from datetime import date

from django import forms
from django.forms import DateInput

from inventory.models import Section


class StocktakingForm(forms.Form):

    counted = forms.IntegerField(label="quantity", min_value=0)


class BrowseStockForm(forms.Form):
    search_from = forms.DateField(initial=date.today(),
                                  widget=DateInput(attrs={'class': 'datepicker'}))
    search_to = forms.DateField(initial=date.today(),
                                widget=DateInput(attrs={'class': 'datepicker'}))
    user = forms.CharField(required=False, max_length=30)
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label="section")
