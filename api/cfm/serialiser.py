from rest_framework import serializers
from . models import *

class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only = True)
    class Meta:
        model = Order
        fields = ["id", "items", "created_at", "owner", "completed", "updated_at"]