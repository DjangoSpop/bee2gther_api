from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.ReadOnlyField(source='seller.username')
    images = serializers.ImageField(required=False)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'min_quantity', 'discounted_price', 'buy_now_price', 
                  'category', 'size', 'stock', 'images', 'seller', 'created_at']
        read_only_fields = ['id', 'seller', 'created_at']
        
        def create(self,validated_data):
            images = validated_data.pop('images', None)
            product = Product.objects.create(**validated_data)
            if images:
                product.images = images 
                product.save()
            return product