from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class UpperCaseCharField(models.CharField):

    def __init__(self, *args, **kwargs):
        super(UpperCaseCharField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if value:
            value = value.upper()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(UpperCaseCharField, self).pre_save(model_instance, add)


class Category(models.Model):
    name = UpperCaseCharField(default='', max_length=40, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Categories"


class Manufacturer(models.Model):
    name = UpperCaseCharField(default='', max_length=40, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ItemLocation(models.Model):
    section = models.ForeignKey('section')
    item = models.ForeignKey('item')
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, default=1)


class Section(models.Model):
    name = UpperCaseCharField(default='', max_length=40, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = UpperCaseCharField(default='', max_length=40)
    category = models.ManyToManyField(Category, related_name='category')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='manufacturer')
    section = models.ManyToManyField(Section, through=ItemLocation)

    def __str__(self):
        return str(self.name) + ' ' + str(self.manufacturer)

    class Meta:
        unique_together = ('name', 'manufacturer')
        ordering = ('name',)
