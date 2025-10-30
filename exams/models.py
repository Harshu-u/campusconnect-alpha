from django.db import models
from courses.models import Course
from students.models import Student

class Examination(models.Model):
    TYPE_CHOICES = (
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
    )
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="examinations")
    exam_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    room = models.CharField(max_length=20, blank=True, null=True)
    max_marks = models.IntegerField(blank=True, null=True)
    academic_year = models.CharField(max_length=10)
    semester = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.course.name})"

class ExamResult(models.Model):
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name="results")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="exam_results")
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    grade = models.CharField(max_length=5, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)