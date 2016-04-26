from django import forms
from django.forms import BaseFormSet, formsets

from .models import Column, Table


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ('name',)


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        #fields = ('column_name', 'datatype', 'options')
        fields = '__all__'

class OutputForm(forms.Form):
    output = forms.CharField(widget=forms.Textarea, label='SQL output')
    fields = ('output',)

class BaseColumnFormset(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        column_nameAll = []
        datatypeAll = []
        optionsAll = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                column_name = form.cleaned_data['column_name']
                datatype = form.cleaned_data['datatype']
                options = form.cleaned_data['options']

                if column_name and datatype and options:
                    if column_name in column_nameAll:
                        duplicates = True
                    column_nameAll.append(column_name)

                    if datatype in datatypeAll:
                        duplicates = True
                    datatypeAll.append(datatype)

                    if options in optionsAll:
                        duplicates = True
                    optionsAll.append(options)

                    if duplicates:
                        raise forms.ValidationError('Columns have to be unique.', code='duplicates')

                    if not datatype:
                        raise forms.ValidationError('Columns must have datatype.', code='missing_datatype')

                    elif not column_name:
                        raise forms.ValidationError('Columns must have name.', code='missing_column_name')

ColumnFormset = formsets.formset_factory(ColumnForm, formset=BaseColumnFormset)

