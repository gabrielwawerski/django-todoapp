from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from core import config
from core.models import ListEntry


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ListEntryForm(forms.Form):
    entry_text = forms.CharField(max_length=config.ENTRY_TEXT_MAX_LENGTH, label="Add task")


class ListForm(forms.Form):
    list_name = forms.CharField(max_length=config.LIST_NAME_MAX_LENGTH)
    entry_text = forms.CharField(max_length=config.ENTRY_TEXT_MAX_LENGTH)

    def clean_list_name(self):
        data = self.cleaned_data['list_name']

        if len(data) == 0:
            raise ValidationError('List name cannot be empty.')
        elif len(data) <= 2:
            raise ValidationError('List name is too short.')
        return data
