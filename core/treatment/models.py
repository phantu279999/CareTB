from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import TimeStampedModel
from core.customer.models import Customer
from core.product.models import Service, Product
from core.general.models import CustomUser, TimeFrame, DiscountCode


# Lịch hen
class Appointment(TimeStampedModel):
    STATUS_CHOICES = (
        ('scheduled', _('Scheduled')),
        ('confirmed', _('Confirmed')),
        ('completed', _('Completed')),
        ('canceled', _('Canceled')),
        ('no_show', _('No Show')),
    )

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='appointments', verbose_name=_('Customer')
    )
    doctor = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="doctor_appointments", verbose_name=_("Doctor")
    )
    date = models.DateField(verbose_name=_("Date"))
    time_frame = models.ForeignKey(
        TimeFrame, on_delete=models.SET_NULL, null=True, verbose_name=_("Time Slot")
    )
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="scheduled", verbose_name=_("Status")
    )
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    services = models.ManyToManyField(
        Service, blank=True, related_name="appointments", verbose_name=_("Services"))

    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")

    def __str__(self):
        return f"{self.customer or 'Unknown Customer'} - {self.date} - {self.time_frame or 'Unknown Time'}"


class TreatmentProcess(TimeStampedModel):
    STATUS_CHOICES = (
        ('experience_required', _('Yêu cầu trải nghiệm')),
        ('service_required', _('Yêu cầu dịch vụ')),
        ('waiting_for_nurse', _('Chờ y tá tiếp nhận')),
        ('waiting_for_doctor', _('Chờ bác sĩ thăm khám')),
        ('waiting_for_expert', _('Chờ chuyên gia chỉ định')),
        ('therapy', _('Trị liệu')),
        ('re_examination', _('Tái khám')),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='treatment_processes',
                                 verbose_name=_("Customer"))
    name = models.CharField(max_length=100, verbose_name=_("Process Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    expected_end_date = models.DateField(null=True, blank=True, verbose_name=_("Expected End Date"))
    actual_end_date = models.DateField(null=True, blank=True, verbose_name=_("Actual End Date"))
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='experience_required',
                              verbose_name=_("Status"))
    assigned_doctor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                                        related_name='assigned_processes',
                                        verbose_name=_("Assigned Doctor"))

    class Meta:
        verbose_name = _("Treatment Process")
        verbose_name_plural = _("Treatment Processes")

    def __str__(self):
        return f"{self.customer} - {self.name}"


class TreatmentSession(TimeStampedModel):
    STATUS_CHOICES = (
        ('scheduled', _('Scheduled')),
        ('completed', _('Completed')),
        ('canceled', _('Canceled')),
    )

    treatment_process = models.ForeignKey(TreatmentProcess, on_delete=models.CASCADE,
                                          related_name='sessions', verbose_name=_("Treatment Process"))
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='treatment_session', verbose_name=_("Appointment"))
    session_number = models.PositiveIntegerField(verbose_name=_("Session Number"))
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled',
                              verbose_name=_("Status"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    services_performed = models.ManyToManyField(Service, blank=True,
                                                related_name='treatment_sessions',
                                                verbose_name=_("Services Performed"))

    class Meta:
        verbose_name = _("Treatment Session")
        verbose_name_plural = _("Treatment Sessions")
        constraints = [
            models.UniqueConstraint(
                fields=['treatment_process', 'session_number'],
                name='unique_session_per_treatment'
            )
        ]

    def __str__(self):
        return f"{self.treatment_process} - Session {self.session_number}"


class Invoice(TimeStampedModel):
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('pending', _('Pending')),
        ('paid', _('Paid')),
        ('canceled', _('Canceled')),
        ('refunded', _('Refunded')),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices',
                                 verbose_name=_("Customer"))
    invoice_number = models.CharField(max_length=20, unique=True, verbose_name=_("Invoice Number"))
    date = models.DateField(verbose_name=_("Invoice Date"))
    due_date = models.DateField(verbose_name=_("Due Date"))
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft',
                              verbose_name=_("Status"))
    discount = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name=_("Discount"))
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                          verbose_name=_("Discount Amount"))
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                   verbose_name=_("Tax Rate"))
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                     verbose_name=_("Tax Amount"))
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Subtotal"))
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Total"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    def __str__(self):
        return f"{self.invoice_number} - {self.customer}"

    def save(self, *args, **kwargs):
        self.subtotal = sum(item.total for item in self.items.all())
        self.tax_amount = self.subtotal * (self.tax_rate / 100)
        self.total = self.subtotal + self.tax_amount - self.discount_amount
        super().save(*args, **kwargs)


class InvoiceItem(TimeStampedModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items',
                                verbose_name=_("Invoice"))
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("Service"))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("Product"))
    description = models.CharField(max_length=255, verbose_name=_("Description"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Price"))
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                   verbose_name=_("Item Discount"))
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Item Tax"))
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Item Total"))

    class Meta:
        verbose_name = _("Invoice Item")
        verbose_name_plural = _("Invoice Items")

    def __str__(self):
        return f"{self.description} - {self.quantity} x {self.price}"

    def save(self, *args, **kwargs):
        old_total = self.total
        self.total = (self.price * self.quantity) + self.tax - self.discount
        super().save(*args, **kwargs)

        if old_total != self.total:
            self.invoice.save()


class TreatmentReport(TimeStampedModel):
    treatment_process = models.ForeignKey(TreatmentProcess, on_delete=models.CASCADE,
                                          related_name='reports', verbose_name=_("Treatment Process"))
    report_date = models.DateField(verbose_name=_("Report Date"))
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    content = models.TextField(verbose_name=_("Content"))
    doctor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                               related_name='authored_reports', verbose_name=_("Doctor"))

    class Meta:
        verbose_name = _("Treatment Report")
        verbose_name_plural = _("Treatment Reports")

    def __str__(self):
        return f"{self.treatment_process} - {self.report_date}"