from django import forms
from django.forms import formsets

from .models import Table


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = '__all__'


TableFormset = formsets.formset_factory(TableForm)
