from django.db import models
from core.models import User
from students.models import Department
from django.utils.translation import gettext_lazy as _

class Faculty(models.Model):
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('terminated', 'Terminated'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    
    # --- THIS IS THE FIX ---
    # Increased max_length from 20 to 100 to fit your existing data.
    faculty_id = models.CharField(max_length=100, unique=True, verbose_name=_("Faculty ID"))
    # --- END FIX ---
    
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='faculty_members', verbose_name=_("Department"))
    
    designation = models.CharField(max_length=100, verbose_name=_("Designation"))
    specialization = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Specialization"))
    
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Phone Number"))
    office_location = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Office Location"))
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name=_("Status"))
    date_of_joining = models.DateField(null=True, blank=True, verbose_name=_("Date of Joining"))

    class Meta:
        verbose_name = _("Faculty")
        verbose_name_plural = _("Faculty")
        ordering = ['faculty_id']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.faculty_id})"