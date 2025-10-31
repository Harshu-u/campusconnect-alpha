from django.db import models
from courses.models import Course
from faculty.models import Faculty

class Timetable(models.Model):
    DAY_CHOICES = (
        (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'),
        (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetable_entries')
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='timetable_entries')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=10)
    semester = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.course_code} on {self.get_day_of_week_display()} at {self.start_time}"