from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from products.views import StandardResultsSetPagination
from .models import GroupBuy, GroupBuyParticipation
from .serializers import GroupBuySerializer, GroupBuyParticipation, GroupBuyParticipationSerializer
from products.models import Product
from django.views.generic import ListView, DetailView
from django.views import View
from django.shortcuts import redirect
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from .models import GroupBuy, GroupBuyParticipation
from django.http import HttpResponseBadRequest
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
        
        serializer = GroupBuyParticipationSerializer(data=request.data)
        if serializer.is_valid():
            participation, created = GroupBuyParticipation.objects.get_or_create(
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
        participations = GroupBuyParticipation.objects.filter(group_buy=group_buy)
        serializer = GroupBuyParticipationSerializer(participations, many=True)
        return Response(serializer.data)
    
class ParticipationViewSet(viewsets.ModelViewSet):
    queryset = GroupBuyParticipation.objects.all()
    serializer_class = GroupBuyParticipationSerializer
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

class GroupListView(ListView):
    model = GroupBuy
    template_name = 'groupbuys/groupbuy_list.html'
    context_object_name = 'groupbuys'
class GroupBuyDetailView(ListView):
    model = GroupBuy
    template_name = 'groupbuys/group_detail.html'
    context_object_name = 'groupbuys'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_in_groupbuy'] = GroupBuyParticipation.objects.filter(
                group_buy=self.object,
                user=self.request.user
            ).exists()
        return context

class joinGroupView(View):
    def post(self, request, pk):
        groupbuy = GroupBuy.objects.get(pk=pk)
        return redirect('groupbuy-detail', pk=pk)


class JoinGroupBuyView(LoginRequiredMixin, View):
    def post(self, request, pk):
        groupbuy = get_object_or_404(GroupBuy, pk=pk)

        if groupbuy.is_closed:
            messages.error(request, "This group buy is already closed.")
            return redirect('groupbuy-detail', pk=pk)

        if GroupBuyParticipation.objects.filter(group_buy=groupbuy, user=request.user).exists():
            messages.warning(request, "You are already part of this group buy.")
            return redirect('groupbuy-detail', pk=pk)

        try:
            with transaction.atomic():
                # Check if there's still space in the group buy
                if groupbuy.participants < groupbuy.target_participants:
                    # Create a new participant entry
                    GroupBuyParticipation.objects.create(
                        group_buy=groupbuy,
                        user=request.user
                    )

                    # Increment the participant count
                    groupbuy.participants += 1
                    groupbuy.save()

                    # Check if the target has been reached
                    if groupbuy.participants == groupbuy.target_participants:
                        groupbuy.is_closed = True
                        groupbuy.save()
                        # Here you might want to trigger some additional logic,
                        # like notifying all participants or processing orders

                    messages.success(request, "You have successfully joined the group buy!")
                else:
                    messages.error(request, "This group buy is already full.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('groupbuy-detail', pk=pk)