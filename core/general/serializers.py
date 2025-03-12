from rest_framework import serializers
from .models import (
    PermissionCategory, CustomPermission, CustomUser, Contour,
    SourceToCustomer, DiscountCode, CommissionLevel, Department, TimeFrame
)


class PermissionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionCategory
        fields = ['id', 'name']


class CustomPermissionSerializer(serializers.ModelSerializer):
    category = PermissionCategorySerializer()

    class Meta:
        model = CustomPermission
        fields = ['id', 'category', 'name']


class CustomUserSerializer(serializers.ModelSerializer):
    permissions = CustomPermissionSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'full_name', 'phone', 'user_type', 'permissions']


class ContourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        fields = ['id', 'code', 'name', 'time_setting', 'description']


class SourceToCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceToCustomer
        fields = ['id', 'name']


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ['id', 'code', 'name', 'type', 'applicable_level', 'start_date', 'end_date']


class CommissionLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionLevel
        fields = ['id', 'level']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'position']


class TimeFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeFrame
        fields = ['id', 'start_time', 'end_time']
