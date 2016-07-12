from django.forms import formsets, BaseFormSet, models
from django.shortcuts import render, render_to_response
from django.db import connection

from generator.models import Table, Column, Name, Surname, Datatype
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
            # print(table)
            column_formset = ColumnFormset(request.POST, request.FILES, prefix='column_formset')
            if column_formset.is_valid():
                for form in column_formset.forms:
                    column = form.save(commit=False)
                    column.table = table
                    column.save()
                    # print(column)
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
                  {'table_form': table_form, 'column_formset': column_formset})


def generate_sql(request, table):
    return render(request, 'generator/generate_sql.html', dict(generated_sql=build_insert(table)))


def build_insert(table, rows_number=5):
    columns = Column.objects.filter(table=table)
    # names = Name.objects.order_by('?')[:rows_number]
    # surnames = Surname.objects.order_by('?')[:rows_number]
    insertSQL = ''
    columns_names = ', '.join(str(column.column_name) for column in list(columns.all()))
    cursor = connection.cursor()
    # tables = connection.introspection.table_names()
    # print(tables)
    # seen_models = connection.introspection.installed_models(tables)
    # print(seen_models)
    cursor.execute('SELECT * FROM generator_name')
    print(cursor.fetchall())
    for col in list(columns.all()):
        pass
        # print(str(Datatype.objects.filter(datatype=col.datatype)))
    # datatypes = list(Datatype.objects.filter(id=int(column.datatype)) for column in list(columns.all()))
    for counter in range(0, rows_number):
        insertSQL += 'Insert into ' + table.name + ' (' + columns_names + ') values ();\n'
    return insertSQL


def set_up_configuration(request):
    return render(request, 'generator/set_up_configuration.html',
                  dict(tables=Table.objects.all(), columns=Column.objects.all()))
