from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'add_to_section', views.add_to_section, name='add_to_section'),
    url(r'new_item', views.new_item, name='new_item'),
    url(r'show_items', views.show_items, name='show_items'),
    url(r'add_category', views.add_category, name='add_category'),
    url(r'add_manufacturer', views.add_manufacturer, name='add_manufacturer'),
    url(r'new_section', views.new_section, name='new_section'),
    url(r'stocktaking', views.stocktaking, name='stocktaking'),



]