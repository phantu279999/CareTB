from core.common.serializers import DynamicFieldsModelSerializer
from .models import (
    Appointment,
    TreatmentProcess,
    TreatmentSession,
    Invoice,
    InvoiceItem,
    TreatmentReport
)


class AppointmentSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class TreatmentSessionSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = TreatmentSession
        fields = '__all__'


class TreatmentProcessSerializer(DynamicFieldsModelSerializer):
    sessions = TreatmentSessionSerializer(many=True, read_only=True)

    class Meta:
        model = TreatmentProcess
        fields = '__all__'


class InvoiceItemSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'


class InvoiceSerializer(DynamicFieldsModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'

    def get_total(self, obj):
        return obj.subtotal + obj.tax_amount - obj.discount_amount


class TreatmentReportSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = TreatmentReport
        fields = '__all__'
