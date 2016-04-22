from django.conf.urls import url

from .forms import TableFormset
from . import views

urlpatterns = [
    url(r'^$', views.formset, {'formset_class': TableFormset, 'template': 'generator/generate_new.html'},
        name='generate_new'),
    url(r'', views.generate_new, name='generate_new'),
]
