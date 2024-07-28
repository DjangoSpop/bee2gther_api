# serializers.py

from rest_framework import serializers
from .models import Cart, CartItem, Product

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'added_at']

    def get_product(self, obj):
        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'price': obj.product.price,
            'image': obj.product.image.url if obj.product.image else None
        }
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'added_at']
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total', 'created_at', 'updated_at']

    def get_total(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())