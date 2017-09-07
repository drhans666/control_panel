from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from inventory import views

router = routers.DefaultRouter()
router.register(r'items', views.ItemViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^inventory/', include('inventory.urls', namespace='inventory')),
    url(r'^announcements/', include('announcements.urls', namespace='announcements')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^stocktaking/', include('stocktaking.urls', namespace='stocktaking')),
    url(r'^rest/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'', include('panel.urls', namespace='panel')),

]
