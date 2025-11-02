from django.contrib import admin
from .models import TimetableSlot

@admin.register(TimetableSlot)
class TimetableSlotAdmin(admin.ModelAdmin):
    list_display = (
        'department', 'year', 'semester', 'course', 
        'day_of_week', 'start_time', 'end_time', 'faculty', 'room_number'
    )
    list_filter = ('department', 'year', 'semester', 'day_of_week', 'faculty')
    search_fields = (
        'course__title', 'course__code', 'faculty__user__username', 
        'department__name', 'room_number'
    )
    ordering = ('department', 'year', 'semester', 'day_of_week', 'start_time')