from datetime import date
from django.forms import ModelForm
from .models import Vacation
from django import forms
from django.forms import DateInput


class VacationForm(ModelForm):

    def clean(self):
        cleaned_data = super(VacationForm, self).clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError('End date must be greater then start date')

    class Meta:
        model = Vacation
        widgets = {
            'start_date': forms.DateInput(attrs={'class':'datepicker'}),
            'end_date': forms.DateInput(attrs={'class':'datepicker'})
        }
        fields = '__all__'
        exclude = ['accepted', 'user', 'vac_days']


class VacQuery(forms.Form):
    query_user = forms.CharField(label=False, required=False, max_length=30)
    accepted = forms.ChoiceField(label=False, choices=(('All', ("All")),
                                          (False, ("Not Accepted")),
                                          (True, ("Accepted"))))
    search_from = forms.DateField(label=False, initial=date.today(),
                                  widget=DateInput(attrs={'class': 'datepicker'}))
    search_to = forms.DateField(label=False, initial=date.today(),
                                widget=DateInput(attrs={'class': 'datepicker'}))


class VacVerify(forms.Form):
    decision = forms.ChoiceField(label=False, choices=((True, ("Accept")),
                                          (False, ("Refuse")),
                                          ('delete', ("Delete"))))
