from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import TimeStampedModel
from core.general.models import CustomUser


class Service(TimeStampedModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Service Name"))
    price = models.IntegerField()
    unit = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    content = models.TextField()

    effect = models.CharField(max_length=30)

    sub_services = models.ManyToManyField("self", blank=True, symmetrical=False)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self):
        return self.name

    def get_total_money(self):
        return sum(service.price for service in self.sub_services.all())


class Product(TimeStampedModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    effect = models.CharField(max_length=30)
    import_price = models.IntegerField()
    selling_price = models.IntegerField()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

class Supplier(TimeStampedModel):
    code = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Supplier Name"))
    tax_code = models.IntegerField(blank=True, verbose_name=_("Tax Code"))
    contact_person = models.CharField(max_length=100, blank=True, verbose_name=_("Contact Person"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    address = models.CharField(max_length=50, blank=True, verbose_name=_("Address"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")

    def __str__(self):
        return self.name


class TechnicalProduct(TimeStampedModel):
    STATUS_TECH = (
        ('work', 'Hoạt động'),
        ('inactive', 'Không hoạt động'),
    )

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    time = models.CharField(max_length=30)
    price = models.IntegerField()
    status = models.CharField(max_length=30, choices=STATUS_TECH, default='work')


class Material(TimeStampedModel):
    STATUS_MATERIAL = (
        ('new', 'New'),
        ('used', 'Used'),
        ('old', 'Old'),
    )
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, verbose_name=_("Material Name"))
    origin = models.CharField(max_length=100, verbose_name=_("Origin"))

    quantity = models.IntegerField(verbose_name=_("Quantity"))
    unit = models.CharField(max_length=30, verbose_name=_("Unit"))
    price = models.IntegerField(verbose_name=_("Price"))
    status = models.CharField(max_length=10, choices=STATUS_MATERIAL, default='new', verbose_name=_("Status"))
    is_failure = models.BooleanField(default=False, verbose_name=_("Is Failure"))

    effect = models.CharField(max_length=30, verbose_name=_("Effect"))
    reason_failure = models.TextField(blank=True, verbose_name=_("Reason Failure"))

    import_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")

    def __str__(self):
        return self.name


class Maintenance(TimeStampedModel):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="maintenances")
    times = models.IntegerField()
    date = models.DateField()
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30)

    def __str__(self):
        return f"Maintenance {self.times} for {self.material.name}"


class RepairHistory(TimeStampedModel):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="repair_histories")
    times = models.IntegerField()
    date = models.DateField()
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30)

    def __str__(self):
        return f"Repair {self.times} for {self.material.name}"


class Warehouse(TimeStampedModel):
    STATUS_CHOICES = [
        ("import", "Nhập kho"),
        ("export", "Xuất kho"),
        ("stock", "Tồn kho"),
    ]
    UNIT_TYPE = [
        ('piece', 'Cái'),
        ('box', 'Hộp')
    ]
    code = models.CharField(max_length=10, unique=True)
    material = models.OneToOneField(Material, on_delete=models.CASCADE, related_name="warehouse")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="warehouses")
    creator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="created_warehouses")
    reviewer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="reviewed_warehouses")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="stock")
    import_date = models.DateField(blank=True, null=True)
    shipment_date = models.DateField(blank=True, null=True)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=30, default="piece", choices=UNIT_TYPE)
    unit_price = models.IntegerField(default=0)

    def __str__(self):
        return self.code


