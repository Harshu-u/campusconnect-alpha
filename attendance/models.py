from django.db import models
from students.models import Student
from courses.models import Course
from faculty.models import Faculty

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
        ('on_duty', 'On Duty'),
    )

    # Basic Attendance Information
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    # Time Information
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    
    # Additional Information
    marked_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name="attendance_marked")
    remarks = models.TextField(blank=True, null=True)
    evidence = models.FileField(upload_to='attendance/evidence/', blank=True, null=True)
    
    # For Excused/On Duty Cases
    reason = models.CharField(max_length=200, blank=True, null=True)
    approved_by = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        related_name="attendance_approvals",
        blank=True
    )
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        related_name="attendance_modifications",
        blank=True
    )

    class Meta:
        ordering = ['-date', 'course', 'student']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['student', 'course']),
            models.Index(fields=['status']),
        ]
        unique_together = ['student', 'course', 'date']

    def __str__(self):
        return f"{self.student} - {self.course} ({self.date})"

    def save(self, *args, **kwargs):
        # Calculate duration if time_in and time_out are provided
        if self.time_in and self.time_out:
            from datetime import datetime, date
            time_in = datetime.combine(date.today(), self.time_in)
            time_out = datetime.combine(date.today(), self.time_out)
            self.duration = time_out - time_in
        
        # Update student's attendance percentage
        super().save(*args, **kwargs)
        self.student.calculate_attendance()

    @property
    def is_modifiable(self):
        """
        Determines if the attendance record can still be modified
        Returns False if more than 48 hours have passed
        """
        from django.utils import timezone
        from datetime import timedelta
        return timezone.now() - self.created_at < timedelta(hours=48)

    @property
    def formatted_duration(self):
        if self.duration:
            hours = self.duration.seconds // 3600
            minutes = (self.duration.seconds % 3600) // 60
            return f"{hours}h {minutes}m"
        return "N/A"