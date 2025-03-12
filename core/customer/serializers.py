from rest_framework import serializers
from core.common.serializers import DynamicFieldsModelSerializer
from .models import Customer, MarketingCampaign, CustomerMarketingTracking, Feedback


class CustomerSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class MarketingCampaignSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = MarketingCampaign
        fields = '__all__'


class CustomerMarketingTrackingSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = CustomerMarketingTracking
        fields = '__all__'


class FeedbackSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'