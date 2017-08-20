from datetime import date
from django.forms import ModelForm
from .models import Vacation
from django import forms
from django.contrib.admin.widgets import AdminDateWidget


class VacationForm(ModelForm):
    class Meta:
        model = Vacation
        fields = '__all__'
        exclude = ['accepted', 'user']
        start_date = forms.DateField(widget=AdminDateWidget)
        end_date = forms.DateField(widget=AdminDateWidget)


class VacQuery(forms.Form):
    query_user = forms.CharField(required=False, max_length=30)
    accepted = forms.ChoiceField(choices=(('all', ("All")),
                                          (False, ("Not Accepted")),
                                          (True, ("Accepted"))))
    search_from = forms.DateField(widget=AdminDateWidget, initial=date.today())
    search_to = forms.DateField(widget=AdminDateWidget, initial=date.today())


class VacVerify(forms.Form):
    decision = forms.ChoiceField(choices=((True, ("Accept")),
                                          (False, ("Refuse")),
                                          ('delete', ("Delete"))))

