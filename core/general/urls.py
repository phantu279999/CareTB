from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'permission-categories', PermissionCategoryViewSet)
router.register(r'custom-permissions', CustomPermissionViewSet)
router.register(r'users', CustomUserViewSet)
router.register(r'contours', ContourViewSet)
router.register(r'sources-to-customers', SourceToCustomerViewSet)
router.register(r'discount-codes', DiscountCodeViewSet)
router.register(r'commission-levels', CommissionLevelViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'timeframes', TimeFrameViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
