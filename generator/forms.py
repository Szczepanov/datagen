from django import forms
from django.forms import formsets

from .models import Column, Table


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = '__all__'


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ('column_name', 'datatype', 'options')
        # fields = '__all__'


ColumnFormset = formsets.formset_factory(ColumnForm)
