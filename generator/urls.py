from django.conf.urls import url

from .forms import ColumnFormset
from . import views

urlpatterns = [
    # url(r'^generate_new$', views.formset, {'formset_class': ColumnFormset, 'template': 'generator/generate_new.html'},
    #     name='generate_new'),
    url(r'^', views.multiple_formsets, {'template': 'generator/generate_new.html'},
        name='generate_new'),
]
