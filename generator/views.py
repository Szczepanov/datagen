import json
import random
from copy import deepcopy

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import related
from django.forms import formsets, BaseFormSet
from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic import View

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
    column_formset = ''

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

class Plate(View):
    """
    This class-based-view serves up spaghetti and meatballs.
    Override the following class properties when calling `as_view`:
    * `settings` - sets a view specific to use instead of the `SPAGHETTI_SAUCE` django settings
    * `override_settings` - overrides specified settings from `SPAGHETTI_SAUCE` django settings
    * `plate_template_name` - overrides the template name for the whole view
    * `meatball_template_name` - overrides the template used to render nodes
    For example the below URL pattern would specify a path to a view that displayed
    models from the `auth` app with the given templates::
        url(r'^user_graph/$',
            Plate.as_view(
                settings = {
                    'apps': ['auth'],
                }
                meatball_template_name = "my_app/user_node.html",
                plate_template_name = "my_app/auth_details.html"
        )
    """
    settings = None
    override_settings = {}
    plate_template_name = 'generator/plate.html'
    meatball_template_name = "generator/meatball.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request = None

    def get(self, request):
        return self.plate()

    def plate(self):
        """
        Serves up a delicious plate with your models
        """
        request = self.request
        if self.settings is None:
            graph_settings = deepcopy(getattr(settings, 'SPAGHETTI_SAUCE', {}))
            graph_settings.update(self.override_settings)
        else:
            graph_settings = self.settings

        apps = graph_settings.get('apps', [])

        excludes = [
            "%s__%s" % (app, model)
            for app, models in graph_settings.get('exclude', {}).items()
            for model in models
        ]
        models = ContentType.objects.filter(app_label__in=apps)
        nodes = []
        edges = []
        for model in models:
            if (model.model_class() is None):
                continue
            model.is_proxy = model.model_class()._meta.proxy
            if (model.is_proxy and not graph_settings.get('show_proxy', False)):
                continue

            model.doc = model.model_class().__doc__
            _id = "%s__%s" % (model.app_label, model.model)
            if _id in excludes:
                continue

            label = self.get_node_label(model)

            fields = [f for f in model.model_class()._meta.fields]
            many = [f for f in model.model_class()._meta.many_to_many]
            if graph_settings.get('show_fields', True):
                label += "\n%s\n" % ("-" * len(model.model))
                label += "\n".join([str(f.name) for f in fields])
            edge_color = {'inherit': 'from'}

            for f in fields + many:
                if f.rel is not None:
                    m = f.rel.to._meta
                    to_id = "%s__%s" % (m.app_label, m.model_name)
                    if to_id in excludes:
                        pass
                    elif _id == to_id and graph_settings.get('ignore_self_referential', False):
                        pass
                    else:
                        if m.app_label != model.app_label:
                            edge_color = {'inherit': 'both'}

                        edge = {'from': _id, 'to': to_id, 'color': edge_color}

                        if str(f.name).endswith('_ptr'):
                            # fields that end in _ptr are pointing to a parent object
                            edge.update({
                                'arrows': {'to': {'scaleFactor': 0.75}},  # needed to draw from-to
                                'font': {'align': 'middle'},
                                'label': 'is a',
                                'dashes': True
                            })
                        elif type(f) == related.ForeignKey:
                            edge.update({
                                'arrows': {'to': {'scaleFactor': 0.75}}
                            })
                        elif type(f) == related.OneToOneField:
                            edge.update({
                                'font': {'align': 'middle'},
                                'label': '|'
                            })
                        elif type(f) == related.ManyToManyField:
                            edge.update({
                                'color': {'color': 'gray'},
                                'arrows': {'to': {'scaleFactor': 1}, 'from': {'scaleFactor': 1}},
                            })

                        edges.append(edge)
            if model.is_proxy:
                proxy = model.model_class()._meta.proxy_for_model._meta
                model.proxy = proxy
                edge = {
                    'to': _id,
                    'from': "%s__%s" % (proxy.app_label, proxy.model_name),
                    'color': edge_color,
                }
                edges.append(edge)

            all_node_fields = fields
            if graph_settings.get('show_m2m_field_detail', False):
                all_node_fields = fields + many
            nodes.append(
                {
                    'id': _id,
                    'label': label,
                    'shape': 'box',
                    'group': model.app_label,
                    'title': get_template(self.meatball_template_name).render(
                        {'model': model, 'fields': all_node_fields}
                        )
                }
            )

        data = {
            'meatballs': json.dumps(nodes),
            'spaghetti': json.dumps(edges)
        }
        return render(request, self.plate_template_name, data)

    def get_node_label(self, model):
        """
        Defines how labels are constructed from models.
        Default - uses verbose name, lines breaks where sensible
        """
        if model.is_proxy:
            label = "(P) %s" % (model.name.title())
        else:
            label = "%s" % (model.name.title())

        line = ""
        new_label = []
        for w in label.split(" "):
            if len(line + w) > 15:
                new_label.append(line)
                line = w
            else:
                line += " "
                line += w
        new_label.append(line)

        return "\n".join(new_label)