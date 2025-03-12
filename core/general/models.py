from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from core.common.models import TimeStampedModel


class PermissionCategory(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class CustomPermission(TimeStampedModel):
    category = models.ForeignKey(PermissionCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class CustomUser(AbstractUser):
    class Positions(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        DOCTOR = 'doctor', 'Bác sĩ'
        EXPERT = 'expert', 'Chuyên gia'
        RECEPTIONIST = 'receptionist', 'Lễ tân'
        NURSE = 'nurse', 'Y tá'
        ACCOUNTANT = 'accountant', 'Kế toán'
        EMPLOYEE = 'employee', 'Nhân viên'
        COLLABORATOR = 'collaborator', 'Công tác viên'

    user_type = models.CharField(_("Positions"), max_length=20, choices=Positions.choices, default=Positions.EMPLOYEE)

    full_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)

    permissions = models.ManyToManyField(CustomPermission, blank=True)

    REQUIRED_FIELDS = ['user_type']


class Contour(TimeStampedModel):
    class TimeChoices(models.TextChoices):
        TEN_MINUTES = '10m', '10 phút'
        THIRTY_MINUTES = '30m', '30 phút'
        THIRTEEN_MINUTES = '13m', '13 phút'
        ONE_HOUR = '1h', '1 giờ'
        ONE_DAY = '1d', '1 ngày'

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    time_setting = models.CharField(
        max_length=10,
        choices=TimeChoices.choices,
        default=TimeChoices.TEN_MINUTES
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class SourceToCustomer(TimeStampedModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class DiscountCode(TimeStampedModel):
    class Types(models.TextChoices):
        PERCENT = 'percent', 'Phần trăm'
        AMOUNT = 'amount', 'Số tiền'

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=Types.choices, default=Types.AMOUNT)
    applicable_level = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()


class CommissionLevel(TimeStampedModel):
    level = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.level}%"


class Department(TimeStampedModel):
    name = models.CharField(max_length=30)
    position = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TimeFrame(TimeStampedModel):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"
