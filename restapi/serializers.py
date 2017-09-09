from django.contrib.auth.models import User

from rest_framework import serializers

from inventory.models import Item, Category, Manufacturer, Section


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.StringRelatedField(many=True)
    manufacturer = serializers.StringRelatedField()

    class Meta:
        model = Item
        fields = ('id', 'url', 'name', 'category', 'manufacturer')


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'url', 'name')


class ManufacturerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Manufacturer
        fields = ('id', 'url', 'name')


class SectionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Section
        fields = ('id', 'url', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'url', 'username')