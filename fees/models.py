from django.db import models
from students.models import Student
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class FeeStructure(models.Model):
    department = models.ForeignKey('students.Department', on_delete=models.CASCADE)
    year = models.IntegerField(choices=Student.YEAR_CHOICES)
    
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    hostel_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transport_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    exam_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        verbose_name = _("Fee Structure")
        verbose_name_plural = _("Fee Structures")
        unique_together = ('department', 'year')

    def __str__(self):
        return f"{self.department.name} - Year {self.year}"

    @property
    def total_fee(self):
        return self.tuition_fee + self.hostel_fee + self.transport_fee + self.exam_fee

class FeePayment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('waived', 'Waived Off'), # <-- THIS IS THE FIX
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_payments')
    
    academic_year = models.CharField(max_length=9, help_text="e.g., 2024-2025")
    semester = models.IntegerField(verbose_name=_("Semester"))
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Amount Due"))
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Amount Paid"))
    
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateField(null=True, blank=True, verbose_name=_("Date of Payment"))
    
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Transaction ID"))
    
    class Meta:
        verbose_name = _("Fee Payment")
        verbose_name_plural = _("Fee Payments")
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.student} - {self.academic_year} - Sem {self.semester}"

    @property
    def balance_due(self):
        return self.total_amount - self.amount_paid