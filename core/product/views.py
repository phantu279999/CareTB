from rest_framework import viewsets
from .models import Service, Product, Supplier, TechnicalProduct, Material, Warehouse
from core.product.serializers import (
    ServiceSerializer, ProductSerializer, SupplierSerializer,
    TechnicalProductSerializer, MaterialSerializer, WarehouseSerializer
)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class TechnicalProductViewSet(viewsets.ModelViewSet):
    queryset = TechnicalProduct.objects.all()
    serializer_class = TechnicalProductSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
