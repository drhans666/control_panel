from django.contrib import admin

from .models import Item, Category, Section, Manufacturer, Stocktaking, ItemLocation


admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Section)
admin.site.register(Manufacturer)
admin.site.register(Stocktaking)
admin.site.register(ItemLocation)