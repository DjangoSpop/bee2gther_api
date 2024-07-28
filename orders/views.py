from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer
from groupbuys.models import GroupBuy, GroupBuyParticipation
from products.models import Product

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        group_buy_id = self.request.data.get('group_buy')
        quantity = int(self.request.data.get('quantity', 1))

        with transaction.atomic():
            group_buy = GroupBuy.objects.select_for_update().get(id=group_buy_id)
            
            if group_buy.status != 'active':
                raise serializer.ValidationError("This group buy is not active.")
            
            participation, created = GroupBuyParticipation.objects.get_or_create(
                user=self.request.user,
                group_buy=group_buy,
                defaults={'quantity': 0}
            )
            participation.quantity += quantity
            participation.save()

            group_buy.current_quantity += quantity
            group_buy.save()

            total_price = group_buy.product.price * quantity
            order = serializer.save(
                user=self.request.user,
                group_buy=group_buy,
                quantity=quantity,
                total_price=total_price,
                status='pending'
            )

            if group_buy.current_quantity >= group_buy.product.min_quantity:
                self._confirm_group_buy_orders(group_buy)

        return order

    def _confirm_group_buy_orders(self, group_buy):
        group_buy.status = 'completed'
        group_buy.save()
        
        orders = Order.objects.filter(group_buy=group_buy, status='pending')
        for order in orders:
            order.status = 'confirmed'
            order.save()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response({"detail": "Only pending orders can be cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            group_buy = order.group_buy
            group_buy.current_quantity -= order.quantity
            group_buy.save()

            participation = GroupBuyParticipation.objects.get(user=order.user, group_buy=group_buy)
            participation.quantity -= order.quantity
            if participation.quantity <= 0:
                participation.delete()
            else:
                participation.save()

            order.status = 'cancelled'
            order.save()

        return Response({"detail": "Order cancelled successfully."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        order = self.get_object()
        if order.status != 'confirmed':
            return Response({"detail": "Only confirmed orders can be marked as paid."}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'paid'
        order.save()
        return Response({"detail": "Order marked as paid."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def mark_as_shipped(self, request, pk=None):
        order = self.get_object()
        if order.status != 'paid':
            return Response({"detail": "Only paid orders can be marked as shipped."}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'shipped'
        order.save()
        return Response({"detail": "Order marked as shipped."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def mark_as_delivered(self, request, pk=None):
        order = self.get_object()
        if order.status != 'shipped':
            return Response({"detail": "Only shipped orders can be marked as delivered."}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'delivered'
        order.save()
        return Response({"detail": "Order marked as delivered."}, status=status.HTTP_200_OK)