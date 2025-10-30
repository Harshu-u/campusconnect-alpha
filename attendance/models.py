from django.db import models
from students.models import Student
from courses.models import Course
from faculty.models import Faculty

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name="attendance_marked")
    created_at = models.DateTimeField(auto_now_add=True)