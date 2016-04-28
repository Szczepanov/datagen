from django.forms import formsets, BaseFormSet
from django.http import HttpResponseRedirect
from django.shortcuts import render

from generator.models import Table
from .forms import ColumnForm, TableForm


def generate(request):
    return render(request, 'generator/add_table.html', {})


def generate_new(request):
    if request.method == "POST":
        form = ColumnForm(request.POST or None)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.save()
    else:
        form = ColumnForm()
    return render(request, 'generator/add_table.html', {'form': form})


def display_data(request, data, **kwargs):
    # print('[%s]' % ', '.join(map(str, list(data))))
    return render(request, 'generator/posted-data.html', dict(data=data, **kwargs), )


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
            print(table)
            column_formset = ColumnFormset(request.POST, request.FILES, prefix='column_formset')
            if column_formset.is_valid():
                for form in column_formset.forms:
                    column = form.save(commit=False)
                    column.table = table
                    column.save()
                    print(column)
            # return HttpResponseRedirect('thanks')
            # data = []
            # data.append(table_form.cleaned_data)
            # data.append(column_formset.cleaned_data)
            # return display_data(request, data, multiple_formsets=True)

            return generate_sql(request, table)
    else:
        table_form, column_formset = TableForm(prefix='table_form', instance=Table()), \
                                     ColumnFormset(prefix='column_formset', )
    return render(request, template,
                  {'table_form': table_form, 'column_formset': column_formset,})

#TODO modify method (add columns parameter)
def generate_sql(request, table):
    columns = (1, 2, 3, 4, 5)
    return render(request, 'generator/generate_sql.html', dict(generated_sql=build_insert(table, columns)))

#TODO modify method depending on generate_sql modification
def build_insert(table, columns):
    insertSQL = ''
    for counter, column in enumerate(columns):
        insertSQL += 'Insert into ' + table.name + ' values (' + str(
            counter + 100) + ',\'Name\',\'Surname\');\n'
        # for index in range(0,counter):
        #     insertSQL =+ '' | column. | ','
        # insertSQL =+ ');'
    return insertSQL
