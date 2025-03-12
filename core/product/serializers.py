from rest_framework import serializers
from core.product.models import Service, Product, Supplier, TechnicalProduct, Material, Maintenance, RepairHistory, Warehouse


class ServiceSerializer(serializers.ModelSerializer):
    sub_services = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), many=True, required=False
    )

    class Meta:
        model = Service
        fields = '__all__'

    def create(self, validated_data):
        sub_services = validated_data.pop('sub_services', [])
        service = Service.objects.create(**validated_data)
        service.sub_services.set(sub_services)
        return service

    def update(self, instance, validated_data):
        sub_services = validated_data.pop('sub_services', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if sub_services is not None:
            instance.sub_services.set(sub_services)

        return instance

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class TechnicalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalProduct
        fields = '__all__'

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'

class RepairHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairHistory
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    maintenances = MaintenanceSerializer(many=True, required=False)
    repair_histories = RepairHistorySerializer(many=True, required=False)

    class Meta:
        model = Material
        fields = '__all__'

    def create(self, validated_data):
        maintenances_data = validated_data.pop('maintenances', [])
        repair_histories_data = validated_data.pop('repair_histories', [])
        material = Material.objects.create(**validated_data)

        for maintenance_data in maintenances_data:
            Maintenance.objects.create(material=material, **maintenance_data)
        for repair_history_data in repair_histories_data:
            RepairHistory.objects.create(material=material, **repair_history_data)

        return material

    def update(self, instance, validated_data):
        maintenances_data = validated_data.pop('maintenances', None)
        repair_histories_data = validated_data.pop('repair_histories', None)

        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if maintenances_data is not None:
            instance.maintenances.all().delete()
            for maintenance_data in maintenances_data:
                Maintenance.objects.create(material=instance, **maintenance_data)

        if repair_histories_data is not None:
            instance.repair_histories.all().delete()
            for repair_history_data in repair_histories_data:
                RepairHistory.objects.create(material=instance, **repair_history_data)

        return instance


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'
