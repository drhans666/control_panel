from django.contrib import admin

from .models import Item, Category, Section, Manufacturer, ItemLocation


admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Section)
admin.site.register(Manufacturer)
admin.site.register(ItemLocation)