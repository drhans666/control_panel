from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^inventory/', include('inventory.urls', namespace='inventory')),
    url(r'^announcements/', include('announcements.urls', namespace='announcements')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^stocktaking/', include('stocktaking.urls', namespace='stocktaking')),
    url(r'', include('panel.urls', namespace='panel')),

]
