from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^edit_anon/(?P<anon_id>\d+)/$', views.edit_anon, name="edit_anon"),
    url(r'new_anon/', views.new_anon, name='new_anon'),
    url(r'all_anon/', views.all_anon, name='all_anon'),



]