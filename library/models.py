from django.db import models
from students.models import Student

class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True, blank=True, null=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    location = models.CharField(max_length=50, blank=True, null=True)
    publication_year = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BookIssue(models.Model):
    STATUS_CHOICES = (
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="issues")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="book_issues")
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    fine = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='issued')
    created_at = models.DateTimeField(auto_now_add=True)