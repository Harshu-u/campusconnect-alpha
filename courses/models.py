from django.db import models
from students.models import Department
from faculty.models import Faculty
from django.utils.translation import gettext_lazy as _

class Course(models.Model):
    
    COURSE_TYPE_CHOICES = [
        ('theory', 'Theory'),
        ('lab', 'Lab'),
        ('project', 'Project'),
        ('seminar', 'Seminar'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200, verbose_name=_("Course Title"))
    
    # --- THIS IS THE FIX ---
    # We make it nullable so old rows in your database don't cause an error.
    code = models.CharField(max_length=20, unique=True, verbose_name=_("Course Code"), null=True, blank=True)
    # --- END FIX ---
    
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='courses', verbose_name=_("Department"))
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses_taught', verbose_name=_("Lead Faculty"))
    
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    credits = models.IntegerField(verbose_name=_("Credits"))
    
    course_type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES, default='theory', verbose_name=_("Course Type"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name=_("Status"))

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.title}"