from django.db import models
from students.models import Student

class SportsEquipment(models.Model):
    CONDITION_CHOICES = (
        ('excellent', 'Excellent'), ('good', 'Good'),
        ('fair', 'Fair'), ('poor', 'Poor')
    )
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, null=True)
    total_quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField(default=1)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='good')
    location = models.CharField(max_length=50, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SportsEquipmentIssue(models.Model):
    STATUS_CHOICES = ( ('issued', 'Issued'), ('returned', 'Returned'), ('lost', 'Lost') )
    equipment = models.ForeignKey(SportsEquipment, on_delete=models.CASCADE, related_name="issues")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="sports_issues")
    issue_date = models.DateField()
    expected_return_date = models.DateField(blank=True, null=True)
    actual_return_date = models.DateField(blank=True, null=True)
    quantity = models.IntegerField(default=1)
    condition = models.CharField(max_length=10, choices=SportsEquipment.CONDITION_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='issued')
    created_at = models.DateTimeField(auto_now_add=True)