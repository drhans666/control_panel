from django.db import models
from inventory.models import Item, Section
from django.contrib.auth.models import User


class Stocktaking(models.Model):
    stock_id = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, default=1)
    item = models.ForeignKey(Item)
    section = models.ForeignKey(Section)
    stock_quantity = models.IntegerField()
    counted = models.IntegerField()
