from django.conf.urls import url
from . import views


urlpatterns = [
url(r'^vac_edit/(?P<vac_id>\d+)/$', views.vac_edit, name="vac_edit"),
url(r'vac_query', views.vac_query, name='vac_query'),
url(r'vacat_form', views.vacat_form, name='vacat_form'),
url(r'', views.index, name='index'),


]