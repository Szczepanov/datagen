from django import forms

from .models import Column, Table, Project


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


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
