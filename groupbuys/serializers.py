# group_buys/serializers.py
from rest_framework import serializers
from .models import GroupBuy, Participation
from products.serializers import ProductSerializer

class GroupBuySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    current_quantity = serializers.ReadOnlyField()

    class Meta:
        model = GroupBuy
        fields = ['id', 'product', 'end_date', 'current_quantity', 'status', 'created_at', 'updated_at']

class ParticipationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Participation
        fields = ['id', 'user', 'group_buy', 'quantity', 'created_at']