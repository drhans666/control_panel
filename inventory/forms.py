from django import forms
from .models import Item, ItemLocation, Category, Section, Manufacturer


class ItemForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(ItemForm, self).clean()
        name = cleaned_data.get('name').upper()
        manufacturer = cleaned_data.get('manufacturer')
        if Item.objects.filter(name=name, manufacturer=manufacturer).exists():
            raise forms.ValidationError('Item already exists')

    class Meta:
        model = Item
        exclude = ('section',)
        fields = '__all__'
        labels = {'name': '',
                  'category': '',
                  'manufacturer': ''}


class ItemLocationForm(forms.ModelForm):

    class Meta:
        model = ItemLocation
        fields = ['item', 'quantity', 'section']
        labels = {'item': '',
                  'quantity': '',
                  'section': ''}


class CategoryForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        name = cleaned_data.get('name').upper()
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError('Category already exists')

    class Meta:
        model = Category
        fields = '__all__'
        labels = {'name':''}


class ManufacturerForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(ManufacturerForm, self).clean()
        name = cleaned_data.get('name').upper()
        if Manufacturer.objects.filter(name=name).exists():
            raise forms.ValidationError('Manufacturer already exists')

    class Meta:
        model = Manufacturer
        fields = '__all__'
        labels = {'name':''}


class SectionForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(SectionForm, self).clean()
        name = cleaned_data.get('name').upper()
        if Section.objects.filter(name=name).exists():
            raise forms.ValidationError('Section already exists')

    class Meta:
        model = Section
        fields = '__all__'
        labels = {'name':''}


class QueryForm(forms.Form):

    item = forms.CharField(max_length=40, initial='all', label=False)
    manufacturer = forms.CharField(max_length=40, initial='all', label=False)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              widget=forms.CheckboxSelectMultiple,
                                              label=False,
                                              required=False)
    section = forms.ModelMultipleChoiceField(queryset=Section.objects.all(),
                                             widget=forms.CheckboxSelectMultiple,
                                             label=False,
                                             required=False)


class SimpleSearch(forms.Form):

    item = forms.CharField(max_length=40, initial='all', label='')
    manufacturer = forms.CharField(max_length=40, initial='all', label='')
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label="")
