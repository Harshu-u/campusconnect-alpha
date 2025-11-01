from django.db import models
from students.models import Department
from faculty.models import Faculty

from django.conf import settings

class Course(models.Model):
    COURSE_TYPE_CHOICES = (
        ('core', 'Core'),
        ('elective', 'Elective'),
        ('lab', 'Laboratory'),
        ('project', 'Project'),
        ('seminar', 'Seminar'),
    )

    # Basic Course Information
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='courses')
    course_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField()
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES, default='core')
    
    # Academic Details
    credits = models.IntegerField()
    lecture_hours = models.IntegerField(default=0)
    tutorial_hours = models.IntegerField(default=0)
    practical_hours = models.IntegerField(default=0)
    semester = models.IntegerField()
    year = models.IntegerField()
    
    # Prerequisites and Requirements
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='required_for')
    min_cgpa_required = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    max_students = models.IntegerField(default=60)
    
    # Course Material
    syllabus = models.FileField(upload_to='courses/syllabus/', blank=True, null=True)
    reference_books = models.TextField(blank=True, null=True)
    online_resources = models.TextField(blank=True, null=True)
    
    # Assessment
    has_final_exam = models.BooleanField(default=True)
    continuous_assessment = models.BooleanField(default=True)
    practical_assessment = models.BooleanField(default=False)
    assignment_weightage = models.IntegerField(default=20)
    midterm_weightage = models.IntegerField(default=30)
    final_weightage = models.IntegerField(default=50)
    
    # Status and System Fields
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses_updated'
    )

    class Meta:
        ordering = ['department', 'semester', 'course_code']
        indexes = [
            models.Index(fields=['course_code']),
            models.Index(fields=['department', 'semester']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.course_code})"

    def get_current_faculty(self):
        current_assignment = self.faculty_assignments.filter(
            is_active=True
        ).first()
        return current_assignment.faculty if current_assignment else None

    def get_enrolled_students(self):
        from attendance.models import Attendance
        return Attendance.objects.filter(
            course=self
        ).values('student').distinct().count()

    def get_attendance_summary(self):
        from attendance.models import Attendance
        from django.db.models import Count
        return Attendance.objects.filter(
            course=self
        ).values('status').annotate(count=Count('id'))

    @property
    def total_hours(self):
        return self.lecture_hours + self.tutorial_hours + self.practical_hours

    def __str__(self):
        return f"{self.name} ({self.course_code})"

class CourseAssignment(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='course_assignments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='faculty_assignments')
    academic_year = models.CharField(max_length=10)
    semester = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.faculty} -> {self.course}"