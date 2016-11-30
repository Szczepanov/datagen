from django.conf.urls import url
from django.views.generic import TemplateView
from generator.views import Plate
from . import views

urlpatterns = [
    url(r'^add_table/$', views.multiple_formsets, {'template': 'generator/add_table.html'},
        name='add_table'),
    url(r'^add_project/$', views.add_project, {'template': 'generator/add_project.html'}, name='add_project'),
    url(r'^generate_sql/$', TemplateView.as_view(template_name='generator/generate_sql.html'), name='generate_sql'),
    # url(r'^setup/$', TemplateView.as_view(template_name='generator/set_up_configuration.html'), name='set_up_configuration'),
    url(r'^create_model/$', TemplateView.as_view(template_name='generator/create_model.html'), name='create_model'),
    url(r'^setup/$', views.set_up_configuration, name='set_up_configuration'),
    url(r'^plate/$', Plate.as_view(), name='plate'),
    url(r'^example/$', TemplateView.as_view(template_name='generator/example.html')),
    url(r'^$', TemplateView.as_view(template_name='generator/index.html')),
]
