from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'student', 'course', 'status', 'faculty')
    list_filter = ('date', 'status', 'course', 'faculty', 'student__department')
    search_fields = ('student__user__username', 'course__title', 'faculty__user__username')
    autocomplete_fields = ('student', 'course', 'faculty')
    date_hierarchy = 'date'