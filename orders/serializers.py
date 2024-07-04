from rest_framework import serializers
from .models import Order
from groupbuys.models import GroupBuy

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'group_buy', 'quantity', 'total_price', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'total_price', 'status', 'created_at', 'updated_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    group_buy = serializers.PrimaryKeyRelatedField(queryset=GroupBuy.objects.filter(status='active'))

    class Meta:
        model = Order
        fields = ['group_buy', 'quantity']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value