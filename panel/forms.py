from datetime import date
from django.forms import ModelForm
from .models import Vacation
from django import forms


class VacationForm(ModelForm):

    def clean(self):
        cleaned_data = super(VacationForm, self).clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError('End date must be greater then start date')

    class Meta:
        model = Vacation
        fields = '__all__'
        exclude = ['accepted', 'user', 'vac_days']


class VacQuery(forms.Form):
    query_user = forms.CharField(required=False, max_length=30)
    accepted = forms.ChoiceField(choices=(('all', ("All")),
                                          (False, ("Not Accepted")),
                                          (True, ("Accepted"))))
    search_from = forms.DateField(initial=date.today())
    search_to = forms.DateField(initial=date.today())


class VacVerify(forms.Form):
    decision = forms.ChoiceField(choices=((True, ("Accept")),
                                          (False, ("Refuse")),
                                          ('delete', ("Delete"))))
