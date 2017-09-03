from django import forms
from .models import Employee
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        labels = {'username': '', 'password1': '', 'password2': ''}


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = '__all__'
        labels = {'user':'',
                  'section':''}
