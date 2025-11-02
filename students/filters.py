# --- File: students/filters.py ---
# This is the full and correct file.

import django_filters
from .models import Student, Department
from django.db.models import Q

class StudentFilter(django_filters.FilterSet):
    """
    A filter set for the Student model.
    """
    
    # Custom filter for a combined name/ID/email search
    search = django_filters.CharFilter(method='filter_by_search', label="Search")
    
    # Filter by department
    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(),
        field_name='department',
        label='Department'
    )
    
    # Filter by year
    year = django_filters.ChoiceFilter(
        choices=[(i, f'Year {i}') for i in range(1, 5)],
        field_name='year',
        label='Year'
    )
    
    # Filter by section
    section = django_filters.ChoiceFilter(
        choices=Student.SECTION_CHOICES,
        field_name='section',
        label='Section'
    )
    
    # Filter by status
    status = django_filters.ChoiceFilter(
        choices=Student.STATUS_CHOICES,
        field_name='status',
        label='Status'
    )

    class Meta:
        model = Student
        # Define fields that can be filtered on
        fields = ['search', 'department', 'year', 'section', 'status']

    def filter_by_search(self, queryset, name, value):
        """
        Custom method to search across multiple fields.
        """
        if not value:
            return queryset
        
        # Q objects allow for complex "OR" lookups
        return queryset.filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(student_id__icontains=value) |
            Q(user__email__icontains=value)
        )