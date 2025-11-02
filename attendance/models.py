from django.db import models
from students.models import Student
from courses.models import Course
from faculty.models import Faculty
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances')
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, help_text="Faculty member who took the attendance")
    
    date = models.DateField(default=timezone.now, verbose_name=_("Date"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name=_("Status"))
    
    remarks = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Remarks"))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Attendance Record")
        verbose_name_plural = _("Attendance Records")
        # Ensure one student can only have one attendance status for a course on a specific date
        unique_together = ('student', 'course', 'date')
        ordering = ['-date', 'student']

    def __str__(self):
        return f"{self.student} - {self.course.code} on {self.date}: {self.get_status_display()}"