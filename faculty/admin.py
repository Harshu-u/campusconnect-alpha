from django.contrib import admin
from .models import Faculty

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_id', 'user_full_name', 'department', 'designation', 'status')
    list_filter = ('department', 'status', 'designation')
    
    # --- THIS IS THE FIX ---
    # This field is required by AttendanceAdmin's autocomplete
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'faculty_id')
    # --- END FIX ---
    
    autocomplete_fields = ('user', 'department')

    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.short_description = 'Name'