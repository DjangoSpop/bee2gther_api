from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import GroupBuy, Participation
from .serializers import GroupBuySerializer, ParticipationSerializer
from products.models import Product

class GroupBuyViewSet(viewsets.ModelViewSet):
    queryset = GroupBuy.objects.all()
    serializer_class = GroupBuySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        product = Product.objects.get(id=product_id)
        serializer.save(product=product)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def join(self, request, pk=None):
        group_buy = self.get_object()
        quantity = int(request.data.get('quantity', 1))
        
        if group_buy.status != 'active':
            return Response({'detail': 'This group buy is not active.'}, status=status.HTTP_400_BAD_REQUEST)

        participation, created = Participation.objects.get_or_create(
            user=request.user,
            group_buy=group_buy,
            defaults={'quantity': quantity}
        )

        if not created:
            participation.quantity += quantity
            participation.save()

        group_buy.current_quantity += quantity
        if group_buy.current_quantity >= group_buy.product.min_quantity:
            group_buy
