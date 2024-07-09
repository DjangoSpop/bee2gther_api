from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Product
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100





class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    parser_classes = (MultiPartParser, FormParser)
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    @action(detail=False, methods=['get'])
    def my_products(self, request):
        products = Product.objects.filter(seller=request.user)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['post'])
    def add_product(self, request):
        serializer = self.get_serilaizer(data= request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.eerors, status = status.HTTP_201_CREATED)
        return Response(serilaizer.errors, status=status.HTTP_401_REQUEST)
        
    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        product = self.get_object()
        new_stock = request.data.get('stock')
        if new_stock is not None:
            product.stock = new_stock
            product.save()
            return Response({'status': 'stock updated'})
        return Response({'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.seller != request.user:
            return Response({'status': 'unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    