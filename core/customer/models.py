from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import TimeStampedModel
from core.general.models import SourceToCustomer
from core.product.models import Service


class Customer(TimeStampedModel):
    GENDER_CHOICES = (
        ('male', _('Male')),
        ('female', _('Female')),
        ('other', _('Other')),
    )

    STATUS_CHOICES = (
        ('prospect', _('Prospect')),
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('former', _('Former')),
    )

    first_name = models.CharField(max_length=50, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last Name'))
    phone = models.CharField(max_length=10, verbose_name=_('Phone Number'))
    email = models.EmailField(blank=True, verbose_name=_('Email'))
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other', verbose_name=_('Gender'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date of Birth'))
    address = models.TextField(blank=True, verbose_name=_("Address"))
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='prospect', verbose_name=_('Status'))
    source = models.ForeignKey(SourceToCustomer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Source'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class MarketingCampaign(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name=_('Campaign Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(verbose_name=_("End Date"))
    budget = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Budget"))

    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Marketing Campaign")
        verbose_name_plural = _("Marketing Campaigns")

    def __str__(self):
        return self.name


class CustomerMarketingTracking(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='marketing_trackings',
        verbose_name=_("Customer")
    )
    campaign = models.ForeignKey(
        MarketingCampaign,
        on_delete=models.CASCADE,
        related_name='customer_trackings',
        verbose_name=_("Campaign")
    )
    is_contacted = models.BooleanField(default=False, verbose_name=_("Is Contacted"))
    is_interested = models.BooleanField(default=False, verbose_name=_("Is Interested"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    class Meta:
        verbose_name = _("Customer Marketing Tracking")
        verbose_name_plural = _("Customer Marketing Tracking")

    def __str__(self):
        return f"{self.customer} - {self.campaign}"


class Feedback(TimeStampedModel):
    RATING_CHOICES = (
        (1, '1 - Very Poor'),
        (2, '2 - Poor'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name=_("Customer")
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        verbose_name=_("Rating")
    )
    comment = models.TextField(blank=True, verbose_name=_("Comment"))
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feedbacks',
        verbose_name=_("Service")
    )
    is_public = models.BooleanField(default=False, verbose_name=_("Is Public"))

    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")

    def __str__(self):
        return f"{self.customer} - {self.rating}/5"