# --- File: faculty/filters.py ---
# This is the full and correct file.

import django_filters
from .models import Faculty
from students.models import Department
from django.db.models import Q

class FacultyFilter(django_filters.FilterSet):
    """
    A filter set for the Faculty model.
    """
    
    # Custom filter for a combined name/ID/email search
    search = django_filters.CharFilter(method='filter_by_search', label="Search")
    
    # Filter by department
    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(),
        field_name='department',
        label='Department'
    )
    
    # Filter by designation
    designation = django_filters.CharFilter(
        field_name='designation',
        lookup_expr='icontains',
        label='Designation'
    )
    
    # Filter by status
    status = django_filters.ChoiceFilter(
        choices=Faculty.STATUS_CHOICES,
        field_name='status',
        label='Status'
    )

    class Meta:
        model = Faculty
        fields = ['search', 'department', 'designation', 'status']

    def filter_by_search(self, queryset, name, value):
        """
        Custom method to search across multiple fields.
        """
        if not value:
            return queryset
        
        return queryset.filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(employee_id__icontains=value) |
            Q(user__email__icontains=value) |
            Q(specialization__icontains=value)
        )