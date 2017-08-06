from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(default='', max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Categories"


class Manufacturer(models.Model):
    name = models.CharField(default='', max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ItemLocation(models.Model):
    section = models.ForeignKey('section')
    item = models.ForeignKey('item')
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    date_added = models.DateTimeField(auto_now_add=True)


class Section(models.Model):
    name = models.CharField(default='', max_length=40)
    have_item = models.ManyToManyField('Item', through=ItemLocation)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Item(models.Model):
    name = models.CharField(default='', max_length=40)
    category = models.ManyToManyField(Category)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + ' ' + str(self.manufacturer)

    class Meta:
        unique_together = ('name', 'manufacturer')
        ordering = ('name',)
