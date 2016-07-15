import random

from django.forms import formsets, BaseFormSet
from django.shortcuts import render

from generator.models import Table, Column, Name, Surname, Project
from .forms import ColumnForm, TableForm, ProjectForm


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
    return render(request, 'generator/posted_data.html', dict(data=data, **kwargs), )


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

            return generate_sql(request=request, table=table, row_number=request.POST.get('row_number'))
    else:
        table_form, column_formset = TableForm(prefix='table_form', instance=Table()), \
                                     ColumnFormset(prefix='column_formset', )
    return render(request, template,
                  {'table_form': table_form, 'column_formset': column_formset})


def generate_sql(request, table, row_number):
    return render(request, 'generator/generate_sql.html', dict(generated_sql=build_insert(table, row_number)))


def build_insert(table, rows_number=5):
    columns = Column.objects.filter(table=table)
    insertSQL = ''
    columns_names = ', '.join(str(column.column_name) for column in list(columns.all()))
    # cursor = connection.cursor()
    # tables = connection.introspection.table_names()
    # print(tables)
    # seen_models = connection.introspection.installed_models(tables)
    # print(seen_models)
    # cursor.execute('SELECT * FROM generator_name')
    # print(cursor.fetchall())
    auto_increment = 0
    for counter in range(0, int(rows_number)):
        values = []
        SEX = random.sample(['M', 'F'], 1)
        for col in list(columns.all()):
            if str(col.datatype) == 'Name':
                values.append('\'' + str((Name.objects.filter(sex=SEX[0]).order_by('?')[:1])[0].name) + '\'')
            elif str(col.datatype) == 'Surname':
                values.append('\'' + str((Surname.objects.filter(sex=SEX[0]).order_by('?')[:1])[0].surname) + '\'')
            elif str(col.datatype) == 'Auto-increment':
                values.append(str(auto_increment))
                auto_increment += 1
            elif str(col.datatype) == 'Numeric':
                values.append(str(random.randint(18, 99)))
        insertSQL += 'Insert into ' + table.name + ' (' + columns_names + ') values (' + ', '.join(values) + ');\n'
    return insertSQL


def set_up_configuration(request):
    return render(request, 'generator/set_up_configuration.html',
                  dict(tables=Table.objects.all(), columns=Column.objects.all()))


def add_project(request, template):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, prefix='project_form', instance=Project())
        if project_form.is_valid():
            project_form.save(commit=True)
            return render(request, 'generator/add_table.html')
    else:
        project_form = ProjectForm(prefix='project_form', instance=Project())
    return render(request, template, {'project_form': project_form})
