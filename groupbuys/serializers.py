# group_buys/serializers.py
from django.utils import timezone
from rest_framework import serializers

from products.models import Product
from .models import GroupBuy, Participation
from products.serializers import ProductSerializer

class GroupBuySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(), 
        source='product', 
        write_only= True
    )
    product_name = serializers.CharField(source = 'product.name', read_only= True)
    current_quantity = serializers.ReadOnlyField()
    time_left = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = GroupBuy
        fields = [
            'id', 'group', 'product', 'product_name', 'users', 'created_at', 
            'is_active', 'end_date', 'start_time', 'min_quantity', 'max_quantity', 
            'target_quantity', 'current_quantity', 'discount_percentage', 'status',
            'time_left', 'progress_percentage'
        ]
        read_only_fields = ['created_at', 'current_quantity', 'status' ]
    def get_time_left(self, obj):
        now = timezone.now()
        if now > obj.end_time:
            return "Expired"
        time_left = obj.end_time - now
        return str(time_left).split('.')[0]
    
    def get_progress_percentage(self, obj):
        if obj.target_quantity > 0:
            return min(100, int((obj.current_quantity / obj.target_quantity * 100)))
        return 0
    
    def validate(self, data):
        if data.get('end_date') and data.get('start_time'):
            if data['end_date'] <= data['start_time']:
                raise serializers.ValidationError("End date must be after start time")
        if data['min_quantity'] > data['max_quantity']:
            raise serializers.ValidationError("Minimum quantity must be less than maximum quantity.")
        if data['max_quantity'] > data['target_quantity']:
            raise serializers.ValidationError("Maximum quantity must be less than target quantity.")
        return data
    
    def create(self, validated_date):
        return GroupBuy.objects.create(**validated_date)
    
    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.min_quantity = validated_data.get('min_quantity', instance.min_quantity)
        instance.max_quantity = validated_data.get('max_quantity', instance.max_quantity)
        instance.target_quantity = validated_data.get('target_quantity', instance.target_quantity)
        instance.discount_percentage = validated_data.get('discount_percentage', instance.discount_percentage)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
    
class ParticipationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Participation
        fields = ['id', 'user', 'group_buy', 'quantity', 'created_at']