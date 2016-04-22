from django import forms
from django.forms import formsets

from .models import Table


class DataSetForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = '__all__'


DataSetFormset = formsets.formset_factory(DataSetForm)
