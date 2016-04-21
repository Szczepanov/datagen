from django.conf.urls import url

from .forms import DataSetFormset
from . import views

urlpatterns = [
    # url(r'^$', views.generate, name='generate'),
    # url(r'^set_variables*$', views.set_variables, name='set_variables'),
    url(r'^$', views.formset, {'formset_class': DataSetFormset, 'template': 'generator/generate_new.html'},
        name='generate_new'),
    url(r'', views.generate_new, name='generate_new'),
]
