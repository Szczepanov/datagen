from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'', views.multiple_formsets, {'template': 'generator/generate_new.html'},
        name='generate_new'),
]
