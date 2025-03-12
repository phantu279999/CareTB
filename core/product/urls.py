from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.product.views import ServiceViewSet, ProductViewSet, SupplierViewSet, TechnicalProductViewSet, MaterialViewSet, WarehouseViewSet

router = DefaultRouter()
router.register('service', ServiceViewSet, basename='service')
router.register('products', ProductViewSet, basename='product')
router.register('suppliers', SupplierViewSet, basename='supplier')
router.register('technical', TechnicalProductViewSet, basename='technical')
router.register('materials', MaterialViewSet, basename='material')
router.register('warehouse', WarehouseViewSet, basename='warehouse')

urlpatterns = [
    path('', include(router.urls)),
]
