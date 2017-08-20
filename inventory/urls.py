from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'add_to_section', views.add_to_section, name='add_to_section'),
    url(r'new_item', views.new_item, name='new_item'),
    url(r'simple_search', views.simple_search, name='simple_search'),
    url(r'show_items_adv', views.show_items_adv, name='show_items_adv'),
    url(r'add_category', views.add_category, name='add_category'),
    url(r'add_manufacturer', views.add_manufacturer, name='add_manufacturer'),
    url(r'new_section', views.new_section, name='new_section'),
    url(r'show_stocktaking', views.show_stocktaking, name='show_stocktaking'),
    url(r'stock_section', views.stock_section, name='stock_section'),
    url(r'stocktaking/(?P<section>\d+)/', views.stocktaking, name='stocktaking'),

]