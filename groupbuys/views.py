from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from products.views import StandardResultsSetPagination
from .models import GroupBuy, Participation
from .serializers import GroupBuySerializer, ParticipationSerializer
from products.models import Product

class GroupBuyViewSet(viewsets.ModelViewSet):
    queryset = GroupBuy.objects.all()
    serializer_class = GroupBuySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Optionally restricts the returned group buys to a given status,
        by filtering against a `status` query parameter in the URL.
        """
        queryset = GroupBuy.objects.all()
        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset

    def perform_create(self, serializer):
        """
        Create a new group buy and associate it with a product.
        """
        product_id = self.request.data.get('product')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(product=product)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def join(self, request, pk=None):
        """
        Allow a user to join a group buy.
        """
        group_buy = self.get_object()
        quantity = int(request.data.get('quantity', 1))
        
        if group_buy.status != 'active':
            return Response({'detail': 'This group buy is not active.'}, status=status.HTTP_400_BAD_REQUEST)
        if timezone.now() > group_buy.end_date:
            return Response({'detail': 'This group buy has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ParticipationSerializer(data=request.data)
        if serializer.is_valid():
            participation, created = Participation.objects.get_or_create(
                user=request.user,
                group_buy=group_buy,
                defaults={'quantity': quantity}
            )

            if not created:
                participation.quantity += quantity
                participation.save()

            group_buy.current_quantity += quantity
            if group_buy.current_quantity >= group_buy.target_quantity:
                group_buy.status = 'completed'
            group_buy.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        """
        Get all participants for a specific group buy.
        """
        group_buy = self.get_object()
        participations = Participation.objects.filter(group_buy=group_buy)
        serializer = ParticipationSerializer(participations, many=True)
        return Response(serializer.data)
    
class ParticipationViewSet(viewsets.ModelViewSet):
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['put'])
    def update_quantity(self, request, pk=None):
        participation = self.get_object()
        new_quantity = request.data.get('quantity')

        if not new_quantity:
            return Response({"detail": "Quantity is required"}, status=status.HTTP_400_BAD_REQUEST)

        new_quantity = int(new_quantity)
        group_buy = participation.group_buy
        quantity_difference = new_quantity - participation.quantity

        if group_buy.current_quantity + quantity_difference > group_buy.max_quantity:
            return Response({"detail": "Exceeds maximum quantity for this group buy."}, status=status.HTTP_400_BAD_REQUEST)

        participation.quantity = new_quantity
        participation.save()

        group_buy.current_quantity += quantity_difference
        if group_buy.current_quantity >= group_buy.target_quantity:
            group_buy.status = 'completed'
        group_buy.save()

        return Response({"detail": "Quantity updated successfully."}, status=status.HTTP_200_OK)