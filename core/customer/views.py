from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Customer, MarketingCampaign, CustomerMarketingTracking, Feedback
from .serializers import (
    CustomerSerializer,
    MarketingCampaignSerializer,
    CustomerMarketingTrackingSerializer,
    FeedbackSerializer
)
from core.common.permissions import IsAdmin


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'gender', 'source']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    ordering_fields = ['created_at', 'last_name', 'first_name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]

    def get_filtered_customers(self, status):
        queryset = self.queryset.filter(status=status)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def not_bought(self, request):
        return self.get_filtered_customers('prospect')

    @action(detail=False, methods=['GET'])
    def buying(self, request):
        return self.get_filtered_customers('active')

    @action(detail=False, methods=['GET'])
    def bought(self, request):
        return self.get_filtered_customers('former')


class MarketingCampaignViewSet(viewsets.ModelViewSet):
    queryset = MarketingCampaign.objects.all()
    serializer_class = MarketingCampaignSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'end_date', 'name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]


class CustomerMarketingTrackingViewSet(viewsets.ModelViewSet):
    queryset = CustomerMarketingTracking.objects.all()
    serializer_class = CustomerMarketingTrackingSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_contacted', 'is_interested', 'customer', 'campaign']
    ordering_fields = ['created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rating', 'is_public', 'customer', 'service']
    ordering_fields = ['created_at', 'rating']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]
