from django.contrib import admin
from .models import Student, Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head_of_department')
    search_fields = ('name', 'code')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user_full_name', 'department', 'year', 'semester', 'status')
    list_filter = ('department', 'year', 'semester', 'status')
    
    # --- THIS IS THE FIX ---
    # This field is required by AttendanceAdmin's autocomplete
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'student_id')
    # --- END FIX ---
    
    autocomplete_fields = ('user', 'department')
    
    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.short_description = 'Name'