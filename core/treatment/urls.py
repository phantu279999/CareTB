from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AppointmentViewSet,
    TreatmentProcessViewSet,
    TreatmentSessionViewSet,
    InvoiceViewSet,
    InvoiceItemViewSet,
    TreatmentReportViewSet
)

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)
router.register(r'treatment-processes', TreatmentProcessViewSet)
router.register(r'treatment-sessions', TreatmentSessionViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'invoice-items', InvoiceItemViewSet)
router.register(r'reports', TreatmentReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('schedule/', AppointmentViewSet.as_view({'get': 'list'}), name='schedule'),
    path('process/', TreatmentProcessViewSet.as_view({'get': 'list'}), name='process'),
    path('invoices/', InvoiceViewSet.as_view({'get': 'list'}), name='invoices'),
    path('reports/', TreatmentReportViewSet.as_view({'get': 'list'}), name='reports'),
]