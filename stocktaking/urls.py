from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'show_stocktaking', views.show_stocktaking, name='show_stocktaking'),
    url(r'browse_stocktakings', views.browse_stocktakings, name='browse_stocktakings'),
    url(r'stock_section', views.stock_section, name='stock_section'),
    url(r'stocktaking/(?P<section>\d+)/', views.stocktaking, name='stocktaking'),
    ]