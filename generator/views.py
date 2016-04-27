from django.forms import formsets, BaseFormSet
from django.http import HttpResponseRedirect
from django.shortcuts import render

from generator.models import Table
from .forms import ColumnForm, TableForm


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
    # print('[%s]' % ', '.join(map(str, list(data))))
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
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    ColumnFormset = formsets.formset_factory(ColumnForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        table_form = TableForm(request.POST, prefix='table_form', instance=Table())
        if table_form.is_valid():
            table = table_form.save(commit=True)
            column_formset = ColumnFormset(request.POST, request.FILES, prefix='column_formset')
            if column_formset.is_valid():
                for form in column_formset.forms:
                    column = form.save(commit=False)
                    column.table = table
                    column.save()
            return HttpResponseRedirect('thanks')
            # data = []
            # data.append(table_form.cleaned_data)
            # data.append(column_formset.cleaned_data)
            # return display_data(request, data, multiple_formsets=True)
    else:
        table_form, column_formset = TableForm(prefix='table_form', instance=Table()), \
                                     ColumnFormset(prefix='column_formset', )
    return render(request, template,
                  {'table_form': table_form, 'column_formset': column_formset, })
