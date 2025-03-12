from rest_framework import viewsets
from .models import (
    PermissionCategory, CustomPermission, CustomUser, Contour,
    SourceToCustomer, DiscountCode, CommissionLevel, Department, TimeFrame
)
from .serializers import (
    PermissionCategorySerializer, CustomPermissionSerializer, CustomUserSerializer, ContourSerializer,
    SourceToCustomerSerializer, DiscountCodeSerializer, CommissionLevelSerializer, DepartmentSerializer, TimeFrameSerializer
)

class PermissionCategoryViewSet(viewsets.ModelViewSet):
    queryset = PermissionCategory.objects.all()
    serializer_class = PermissionCategorySerializer

class CustomPermissionViewSet(viewsets.ModelViewSet):
    queryset = CustomPermission.objects.all()
    serializer_class = CustomPermissionSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class ContourViewSet(viewsets.ModelViewSet):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer

class SourceToCustomerViewSet(viewsets.ModelViewSet):
    queryset = SourceToCustomer.objects.all()
    serializer_class = SourceToCustomerSerializer

class DiscountCodeViewSet(viewsets.ModelViewSet):
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeSerializer

class CommissionLevelViewSet(viewsets.ModelViewSet):
    queryset = CommissionLevel.objects.all()
    serializer_class = CommissionLevelSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class TimeFrameViewSet(viewsets.ModelViewSet):
    queryset = TimeFrame.objects.all()
    serializer_class = TimeFrameSerializer