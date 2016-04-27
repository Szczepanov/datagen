from django import forms

from .models import Column, Table


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        # fields = ('name',)
        fields = '__all__'


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ('column_name', 'datatype',)
        exclude = ('table',)
