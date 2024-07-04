from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.ReadOnlyField(source='seller.username')

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'min_quantity', 'discounted_price', 'buy_now_price', 
                  'category', 'size', 'stock', 'images', 'seller', 'created_at']
        read_only_fields = ['id', 'seller', 'created_at']