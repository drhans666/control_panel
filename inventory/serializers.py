from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.StringRelatedField(many=True)
    manufacturer = serializers.StringRelatedField()

    class Meta:
        model = Item
        fields = ('id', 'url', 'name', 'category', 'manufacturer')