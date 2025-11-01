from django.db import models
from django.conf import settings
from students.models import Department # Import Department from students app

class Faculty(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('retired', 'Retired'),
        ('on_leave', 'On Leave'),
        ('terminated', 'Terminated'),
    )
    
    EMPLOYMENT_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('visiting', 'Visiting'),
        ('contract', 'Contract'),
    )

    # Basic Information
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="faculty_profile")
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="faculty_members")
    designation = models.CharField(max_length=50)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='full_time')
    
    # Personal Information
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True, null=True)
    personal_email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    
    # Professional Information
    qualification = models.CharField(max_length=200, blank=True, null=True)
    specialization = models.CharField(max_length=200, blank=True, null=True)
    research_interests = models.TextField(blank=True, null=True)
    total_experience = models.DecimalField(max_digits=4, decimal_places=1, help_text="Total years of experience", default=0)
    industry_experience = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    teaching_experience = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    
    # Documents and Verification
    resume = models.FileField(upload_to='faculty/resumes/', blank=True, null=True)
    certificates = models.FileField(upload_to='faculty/certificates/', blank=True, null=True)
    publications = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    
    # Employment Details
    joining_date = models.DateField()
    contract_end_date = models.DateField(blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    bank_account = models.CharField(max_length=50, blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    
    # Status and System Fields
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    is_hod = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_promotion_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['department', 'designation', 'user__first_name']
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['department', 'designation']),
            models.Index(fields=['status']),
        ]
        verbose_name_plural = "Faculty"

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

    def get_courses_taught(self, semester=None):
        from courses.models import CourseAssignment
        assignments = CourseAssignment.objects.filter(faculty=self)
        if semester:
            assignments = assignments.filter(semester=semester)
        return assignments

    def get_total_students(self):
        from courses.models import CourseAssignment
        from students.models import Student
        current_courses = CourseAssignment.objects.filter(faculty=self)
        return Student.objects.filter(
            department=self.department,
            status='active'
        ).count()

    def get_attendance_record(self):
        from attendance.models import Attendance
        from django.db.models import Count
        return Attendance.objects.filter(marked_by=self).values('date').annotate(
            count=Count('id')
        ).order_by('-date')

    @property
    def service_years(self):
        if self.joining_date:
            from datetime import date
            today = date.today()
            years = today.year - self.joining_date.year
            if today.month < self.joining_date.month or (
                today.month == self.joining_date.month and today.day < self.joining_date.day
            ):
                years -= 1
            return years
        return 0

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name} ({self.employee_id})"
        return f"{self.user.username} ({self.employee_id})"
