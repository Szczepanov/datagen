from django import forms

from .models import DataSet


class DataSetForm(forms.ModelForm):
    class Meta:
        model = DataSet
        # field = ('name', 'country', 'column_name', 'data_type', 'rows_number',)
        fields = '__all__'


# class CountryForm(forms.ModelForm):
#     class Meta:
#         model = Country
#         fields = '__all__'
