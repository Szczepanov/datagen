from django import forms
from django.forms import formsets

from .models import DataSet


class DataSetForm(forms.ModelForm):
    class Meta:
        model = DataSet
        fields = '__all__'


DataSetFormset = formsets.formset_factory(DataSetForm)
