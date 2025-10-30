from django.db import models
from students.models import Department, Student

class FeeStructure(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="fee_structures")
    year = models.IntegerField()
    semester = models.IntegerField()
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lab_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    library_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hostel_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    misc_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    academic_year = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-calculate total fee
        self.total_fee = (self.tuition_fee + self.lab_fee + self.library_fee + 
                          self.hostel_fee + self.transport_fee + self.misc_fee)
        super().save(*args, **kwargs)

class FeePayment(models.Model):
    STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('overdue', 'Overdue'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="fee_payments")
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.SET_NULL, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)