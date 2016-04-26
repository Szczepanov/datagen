from django.forms import formsets
from django.shortcuts import render

from generator.models import Table, Column
from .forms import ColumnForm, TableForm, BaseColumnFormset, ColumnFormset


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
    if request.method == 'POST':
        # print('check A')
        # for key in request.POST:
        #     print(key)
        #     value = request.POST[key]
        #     print(value)
        # print('check C')
        table_form, column_formset = \
            TableForm(request.POST or None, prefix='table_form', instance=Table()), \
            ColumnFormset(request.POST or None, prefix='column_formset')
        if table_form.is_valid() and column_formset.is_valid():
            table_form.save()
            for form in column_formset:
                if form:
                    print(form.as_table())
            # for form in column_formset.cleaned_data:
            #     print(form.as_table())
                # column_name = form.cleaned_data.get('column_name')
                # datatype = form.cleaned_data.get('datatype')
                # options = form.cleaned_data.get('options')
                # if column_name and datatype:
                #     new_columns.append(column_name, datatype, options)
            print('check B')
            data = []
            data.append(table_form.cleaned_data)
            data.append(column_formset.cleaned_data)
            print(data)
            return display_data(request, data, multiple_formsets=True)
    else:
        table_form, column_formset = TableForm(prefix='table_form', instance=Table()), \
                                     ColumnFormset(prefix='column_formset', )
    return render(request, template,
                  {'table_form': table_form, 'column_formset': column_formset, })
