from django.shortcuts import render

from generator.models import Table, Column
from .forms import ColumnForm, TableForm, ColumnFormset


def generate(request):
    return render(request, 'generator/generate_new.html', {})


def generate_new(request):
    if request.method == "POST":
        form = ColumnForm(request.POST or None)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.save()
    else:
        form = ColumnForm()
    return render(request, 'generator/generate_new.html', {'form': form})


def display_data(request, data, **kwargs):
    return render(request, 'generator/posted-data.html', dict(data=data, **kwargs), )


def formset(request, formset_class, template):
    if request.method == 'POST':
        formset = formset_class(request.POST or None)
        if formset.is_valid():
            data = formset.cleaned_data
            return display_data(request, data)
    else:
        formset = formset_class()
    return render(request, template, {'formset': formset}, )


def multiple_formsets(request, template):
    table = Table()
    column = Column()
    if request.method == 'POST':
        table_form, column_formset = TableForm(request.POST, prefix='=table_form', instance=table), ColumnFormset(
            request.POST,
            prefix='column_formset')
        if table_form.is_valid() and column_formset.is_valid():
            data = [table_form.cleaned_data, column_formset.cleaned_data]
            return display_data(request, data, multiple_formsets=True)
    else:
        table_form, column_formset = TableForm(prefix='table_form', instance=table), ColumnFormset(
            prefix='column_formset',)
    return render(request, template, {'table_form': table_form, 'column_formset': column_formset})
