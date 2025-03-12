from django.db import models
from django.core.exceptions import ValidationError


from core.general.models import Department


POSITION_CHOICES = [
    ("specialist", "Chuyên viên"),
    ("expert", "Chuyên gia"),
]

CONTRACT_CHOICES = [
    ("official", "Chính thức"),
    ("trial", "Thử việc"),
    ("internship", "Thực tập sinh"),
]

GENDER_CHOICES = [
    ('male', 'Nam'),
    ('female', 'Nữ'),
    ('other', 'Khác'),
]

EDU_CHOICES = [
    ('professor', 'Giáo sư'),
    ('PhD', 'Tiến sĩ'),
    ('master', 'Thạc sĩ'),
    ('university', 'Đại học'),
    ('other', 'Khác'),
]

class Employee(models.Model):
    code = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    contract_file = models.FileField(blank=True, upload_to="contracts/")
    contract_type = models.CharField(max_length=20, choices=CONTRACT_CHOICES)

    contract_term_start_date = models.DateField()
    contract_term_end_date = models.DateField()

    status = models.BooleanField()
    start_date = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    education_level = models.CharField(max_length=20, choices=EDU_CHOICES)

    def clean(self):
        """Ensure contract_term_end_date is after contract_term_start_date"""
        if self.contract_term_end_date and self.contract_term_start_date:
            if self.contract_term_end_date < self.contract_term_start_date:
                raise ValidationError(
                    {"contract_term_end_date": "End date must be after start date"}
                )

    def contract_duration(self):
        """Returns the contract duration in days"""
        return (self.contract_term_end_date - self.contract_term_start_date).days

    def __str__(self):
        return f"{self.full_name} ({self.code}) - {self.position}"


class Collaborator(models.Model):
    code = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.code})"