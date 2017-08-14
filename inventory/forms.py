from django import forms
from .models import Item, ItemLocation, Category, Section, Manufacturer


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        exclude = ('section',)
        fields = '__all__'


class ItemLocationForm(forms.ModelForm):

    class Meta:
        model = ItemLocation
        fields = ['item', 'quantity', 'section']


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'


class ManufacturerForm(forms.ModelForm):

    class Meta:
        model = Manufacturer
        fields = '__all__'


class SectionForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = '__all__'


class QueryForm(forms.Form):

    item = forms.CharField(max_length=40, initial='all')
    manufacturer = forms.CharField(max_length=40, initial='all')
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              widget=forms.CheckboxSelectMultiple,
                                              label="category(optional)",
                                              required=False)
    section = forms.ModelMultipleChoiceField(queryset=Section.objects.all(),
                                             widget=forms.CheckboxSelectMultiple,
                                             label="section(optional)",
                                             required=False)


class StocktakingForm(forms.Form):

    counted = forms.IntegerField(min_value=0)
