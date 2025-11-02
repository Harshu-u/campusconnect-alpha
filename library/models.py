from django.db import models
from students.models import Student
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import datetime

class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    author = models.CharField(max_length=255, verbose_name=_("Author"))
    isbn = models.CharField(max_length=13, unique=True, verbose_name=_("ISBN"))
    publisher = models.CharField(max_length=255, blank=True, verbose_name=_("Publisher"))
    
    total_copies = models.PositiveIntegerField(default=1, verbose_name=_("Total Copies"))
    available_copies = models.PositiveIntegerField(default=1, verbose_name=_("Available Copies"))

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ['title']

    def __str__(self):
        return f"{self.title} by {self.author}"

class BookIssue(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='book_issues')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    
    issue_date = models.DateField(default=timezone.now, verbose_name=_("Issue Date"))
    due_date = models.DateField(verbose_name=_("Due Date"))
    return_date = models.DateField(null=True, blank=True, verbose_name=_("Return Date"))
    
    # Simple fine calculation
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name=_("Fine Amount"))

    class Meta:
        verbose_name = _("Book Issue Record")
        verbose_name_plural = _("Book Issue Records")
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.book.title} issued to {self.student}"
    
    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.issue_date + datetime.timedelta(days=14) # Default 14 day issue
        super().save(*args, **kwargs)