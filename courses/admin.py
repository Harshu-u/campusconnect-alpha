from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'department', 'faculty', 'credits', 'course_type', 'status')
    list_filter = ('department', 'course_type', 'status', 'faculty')
    search_fields = ('title', 'code', 'department__name', 'faculty__user__username')
    ordering = ('code',)

# All other models that no longer exist (like CourseAssignment) have been removed.