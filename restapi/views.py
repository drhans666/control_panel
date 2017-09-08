from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from inventory.models import Item, Category, Manufacturer, Section
from .serializers import ItemSerializer, CategorySerializer, ManufacturerSerializer,\
    SectionSerializer, UserSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('name')
    serializer_class = ItemSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all().order_by('name')
    serializer_class = ManufacturerSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all().order_by('name')
    serializer_class = SectionSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username',)