from django.db import models
from students.models import Department
from faculty.models import Faculty

class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='courses')
    course_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    credits = models.IntegerField()
    semester = models.IntegerField()
    year = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

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