from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.generate, name='generate'),
    url(r'^set_variables*$', views.set_variables, name='set_variables'),
    url(r'^$', views.generate_new, name='generate_new'),
]