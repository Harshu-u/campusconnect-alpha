from django.db import models
from students.models import Student
from courses.models import Course
from django.utils.translation import gettext_lazy as _

class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('midterm_1', 'Mid-Term 1'),
        ('midterm_2', 'Mid-Term 2'),
        ('final', 'Final Exam'),
        ('sessional', 'Sessional'),
        ('practical', 'Practical'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    name = models.CharField(max_length=100, verbose_name=_("Exam Name"))
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES, verbose_name=_("Exam Type"))
    
    exam_date = models.DateField(verbose_name=_("Date of Exam"))
    max_marks = models.PositiveIntegerField(verbose_name=_("Maximum Marks"))

    class Meta:
        verbose_name = _("Exam")
        verbose_name_plural = _("Exams")
        ordering = ['-exam_date', 'course']

    def __str__(self):
        return f"{self.course.code} - {self.get_exam_type_display()}"


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    
    marks_obtained = models.PositiveIntegerField(verbose_name=_("Marks Obtained"))
    
    # A grade, if your system uses them (e.g., A+, B, C)
    grade = models.CharField(max_length=5, blank=True, null=True, verbose_name=_("Grade"))
    
    # Pass/Fail status
    is_pass = models.BooleanField(default=True, verbose_name=_("Pass/Fail Status"))
    
    class Meta:
        verbose_name = _("Result")
        verbose_name_plural = _("Results")
        unique_together = ('student', 'exam') # One result per student per exam
        ordering = ['exam', 'student']

    def __str__(self):
        return f"{self.student} - {self.exam}: {self.marks_obtained}"