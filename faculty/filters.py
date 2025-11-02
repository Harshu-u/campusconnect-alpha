import django_filters
from django import forms
from .models import Faculty, Department
from django.db.models import Q

class FacultyFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_search', 
        label="Search",
        widget=forms.TextInput(attrs={'placeholder': 'Search by Name, ID, or Email...', 'class': 'form-input'})
    )
    
    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Department"
    )

    status = django_filters.ChoiceFilter(
        choices=Faculty.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Status"
    )

    class Meta:
        model = Faculty
        fields = ['search', 'department', 'status']

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        
        return queryset.filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(user__email__icontains=value) |
            Q(faculty_id__icontains=value) |
            Q(designation__icontains=value)
        )