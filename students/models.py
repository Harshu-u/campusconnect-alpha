from django.db import models
from core.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Department Name"))
    code = models.CharField(max_length=20, unique=True, verbose_name=_("Department Code"))
    head_of_department = models.CharField(max_length=150, blank=True, null=True, verbose_name=_("Head of Department"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
        ordering = ['name']

    def __str__(self):
        return self.name

class Student(models.Model):
    
    YEAR_CHOICES = [
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('dropped', 'Dropped'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True, verbose_name=_("Student ID"))
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='students', verbose_name=_("Department"))
    
    year = models.IntegerField(choices=YEAR_CHOICES, verbose_name=_("Year"))
    semester = models.IntegerField(verbose_name=_("Semester"))
    
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Phone Number"))
    address = models.TextField(blank=True, null=True, verbose_name=_("Address"))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_("Date of Birth"))

    # --- FIELDS TO FIX THE ERROR ---
    guardian_name = models.CharField(max_length=150, blank=True, null=True, verbose_name=_("Guardian's Name"))
    guardian_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Guardian's Phone"))
    date_of_admission = models.DateField(default=timezone.now, verbose_name=_("Date of Admission"))
    # --- END FIX ---
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name=_("Status"))
    
    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")
        ordering = ['student_id']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"