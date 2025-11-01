from django.db import models
from django.conf import settings
from core.models import User # Import User from core app

# Department model lives with Student model for now
class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    head_of_department = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('dropped', 'Dropped'),
        ('on_leave', 'On Leave'),
        ('suspended', 'Suspended'),
    )

    SECTION_CHOICES = (
        ('A', 'Section A'),
        ('B', 'Section B'),
        ('C', 'Section C'),
        ('D', 'Section D'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    student_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="students")
    year = models.IntegerField()
    semester = models.IntegerField()
    section = models.CharField(max_length=1, choices=SECTION_CHOICES, default='A')
    enrollment_date = models.DateField()
    expected_graduation = models.DateField(blank=True, null=True)
    
    # Personal Information
    phone = models.CharField(max_length=20, blank=True, null=True)
    alternate_phone = models.CharField(max_length=20, blank=True, null=True)
    personal_email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    nationality = models.CharField(max_length=100, default='Indian')
    
    # Academic Information
    previous_institution = models.CharField(max_length=200, blank=True, null=True)
    previous_qualification = models.CharField(max_length=100, blank=True, null=True)
    previous_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    admission_type = models.CharField(max_length=50, default='regular')  # regular, lateral, transfer
    current_cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    
    # Guardian Information
    guardian_name = models.CharField(max_length=100)
    guardian_relation = models.CharField(max_length=50)
    guardian_phone = models.CharField(max_length=20)
    guardian_email = models.EmailField(blank=True, null=True)
    guardian_occupation = models.CharField(max_length=100, blank=True, null=True)
    guardian_address = models.TextField(blank=True, null=True)
    
    # Additional Information
    hostel_resident = models.BooleanField(default=False)
    transport_user = models.BooleanField(default=False)
    scholarship_status = models.CharField(max_length=50, blank=True, null=True)
    extra_curricular = models.TextField(blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    # Status Information
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['department', 'year', 'section', 'student_id']
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['department', 'year', 'section']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        full_name = self.user.get_full_name()
        return f"{full_name} ({self.student_id})"

    def calculate_attendance(self):
        from attendance.models import Attendance
        total = Attendance.objects.filter(student=self).count()
        if total > 0:
            present = Attendance.objects.filter(
                student=self,
                status__in=['present', 'late']
            ).count()
            self.attendance_percentage = (present / total) * 100
            self.save()
        return self.attendance_percentage

    def get_current_courses(self):
        from courses.models import Course
        return Course.objects.filter(
            department=self.department,
            year=self.year,
            semester=self.semester,
            is_active=True
        )

    def get_attendance_summary(self):
        from attendance.models import Attendance
        from django.db.models import Count
        return Attendance.objects.filter(student=self).values('status').annotate(
            count=Count('id')
        )

    @property
    def is_defaulter(self):
        return self.attendance_percentage < 75.0

    def __str__(self):
        # Check if user has first/last name, otherwise use username
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name} ({self.student_id})"
        return f"{self.user.username} ({self.student_id})"
