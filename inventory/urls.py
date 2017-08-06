from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'add_to_section', views.add_to_section, name='add_to_section'),
    url(r'new_item', views.new_item, name='new_item'),


]