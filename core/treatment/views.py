from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Appointment,
    TreatmentProcess,
    TreatmentSession,
    Invoice,
    InvoiceItem,
    TreatmentReport
)
from .serializers import (
    AppointmentSerializer,
    TreatmentProcessSerializer,
    TreatmentSessionSerializer,
    InvoiceSerializer,
    InvoiceItemSerializer,
    TreatmentReportSerializer
)
from core.common.permissions import (
    IsAdmin,
    IsDoctor,
    IsExpert,
    IsReceptionist,
    IsNurse,
    IsAccountant
)

class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action not in ['list', 'retrieve']:
            permission_classes += self.permission_classes_extra
        return [permission() for permission in permission_classes]


class AppointmentViewSet(BaseViewSet):
    queryset = Appointment.objects.select_related('doctor', 'customer')
    serializer_class = AppointmentSerializer
    filterset_fields = ['status', 'date', 'doctor', 'customer']
    search_fields = ['customer__first_name', 'customer__last_name', 'notes']
    ordering_fields = ['date', 'time_frame']
    permission_classes_extra = [IsAdmin | IsDoctor | IsReceptionist]

    def get_queryset(self):
        queryset = super().get_queryset()
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        return queryset


class TreatmentProcessViewSet(BaseViewSet):
    queryset = TreatmentProcess.objects.select_related('customer', 'assigned_doctor').prefetch_related('sessions')
    serializer_class = TreatmentProcessSerializer
    filterset_fields = ['status', 'customer', 'assigned_doctor']
    search_fields = ['name', 'description', 'customer__first_name', 'customer__last_name']
    ordering_fields = ['start_date', 'expected_end_date', 'actual_end_date']
    permission_classes_extra = [IsAdmin | IsDoctor | IsExpert]


class TreatmentSessionViewSet(BaseViewSet):
    queryset = TreatmentSession.objects.select_related('treatment_process', 'appointment')
    serializer_class = TreatmentSessionSerializer
    filterset_fields = ['status', 'treatment_process', 'appointment']
    ordering_fields = ['session_number']
    permission_classes_extra = [IsAdmin | IsDoctor | IsExpert | IsNurse]


class InvoiceViewSet(BaseViewSet):
    queryset = Invoice.objects.select_related('customer').prefetch_related('items')
    serializer_class = InvoiceSerializer
    filterset_fields = ['status', 'customer', 'date', 'due_date']
    search_fields = ['invoice_number', 'customer__first_name', 'customer__last_name', 'notes']
    ordering_fields = ['date', 'due_date', 'total']
    permission_classes_extra = [IsAdmin | IsAccountant | IsReceptionist]


class InvoiceItemViewSet(BaseViewSet):
    queryset = InvoiceItem.objects.select_related('invoice', 'service', 'product')
    serializer_class = InvoiceItemSerializer
    filterset_fields = ['invoice', 'service', 'product']
    ordering_fields = ['price', 'quantity', 'total']
    permission_classes_extra = [IsAdmin | IsAccountant | IsReceptionist]


class TreatmentReportViewSet(BaseViewSet):
    queryset = TreatmentReport.objects.select_related('treatment_process', 'doctor')
    serializer_class = TreatmentReportSerializer
    filterset_fields = ['treatment_process', 'doctor', 'report_date']
    ordering_fields = ['report_date']
    permission_classes_extra = [IsAdmin | IsDoctor | IsExpert]
