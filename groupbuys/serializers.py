# group_buys/serializers.py
from time import timezone
from rest_framework import serializers
from .models import GroupBuy, Participation
from products.serializers import ProductSerializer

class GroupBuySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    current_quantity = serializers.ReadOnlyField()
    time_left = serializers.SerializerMethodField()
    
    class Meta:
        model = GroupBuy
        fields = ['id', 'product', 'end_date', 'current_quantity','start_time',"end_time",'target_quantity' ,'status', 'created_at', 'updated_at']
    def get_time_left(self, obj):
        now = timezone.now()
        if now > obj.end_time:
            return "Expired"
        time_left = obj.end_time - now
        return str(time_left).split('.')[0]
class ParticipationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Participation
        fields = ['id', 'user', 'group_buy', 'quantity', 'created_at']