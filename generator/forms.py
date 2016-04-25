from django import forms
from django.forms import formsets

from .models import Column, Table


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ('name',)


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ('column_name', 'datatype', 'options')
        # fields = '__all__'


class OutputForm(forms.Form):
    output = forms.CharField(widget=forms.Textarea, label='SQL output')
    fields = ('output', )

ColumnFormset = formsets.formset_factory(ColumnForm, extra=2, )
