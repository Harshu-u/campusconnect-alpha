from django.db import models
from students.models import Department
from courses.models import Course
from faculty.models import Faculty
from django.utils.translation import gettext_lazy as _

class TimetableSlot(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]

    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='timetable_slots')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetable_slots')
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, related_name='timetable_slots')
    
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES, verbose_name=_("Day of Week"))
    start_time = models.TimeField(verbose_name=_("Start Time"))
    end_time = models.TimeField(verbose_name=_("End Time"))
    
    room_number = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Room Number / Location"))
    
    # For differentiating between sections or years of the same department
    year = models.IntegerField(verbose_name=_("Year"), default=1)
    semester = models.IntegerField(verbose_name=_("Semester"), default=1)

    class Meta:
        verbose_name = _("Timetable Slot")
        verbose_name_plural = _("Timetable Slots")
        ordering = ['department', 'year', 'semester', 'day_of_week', 'start_time']

    def __str__(self):
        return f"{self.department} (Year {self.year}) - {self.course.code} on {self.day_of_week} at {self.start_time}"