from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet,
    MarketingCampaignViewSet,
    CustomerMarketingTrackingViewSet,
    FeedbackViewSet
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'marketing-campaigns', MarketingCampaignViewSet)
router.register(r'marketing-tracking', CustomerMarketingTrackingViewSet)
router.register(r'feedbacks', FeedbackViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('marketing/', CustomerViewSet.as_view({'get': 'list'}), name='marketing'),
    path('not-bought/', CustomerViewSet.as_view({'get': 'not_bought'}), name='not-bought'),
    path('buying/', CustomerViewSet.as_view({'get': 'buying'}), name='buying'),
    path('bought/', CustomerViewSet.as_view({'get': 'bought'}), name='bought'),
    path('feedback/', FeedbackViewSet.as_view({'get': 'list'}), name='feedback'),
]