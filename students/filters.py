import django_filters
from django import forms
from .models import Student, Department
from django.db.models import Q

class StudentFilter(django_filters.FilterSet):
    # This 'search' field is not tied to a model field, so we define it manually
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

    year = django_filters.ChoiceFilter(
        choices=Student.YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Year"
    )

    status = django_filters.ChoiceFilter(
        choices=Student.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Status"
    )

    class Meta:
        model = Student
        fields = ['search', 'department', 'year', 'status']

    def filter_search(self, queryset, name, value):
        # This method is called when the 'search' field is used
        # It searches across multiple fields on the related User model and the Student model
        if not value:
            return queryset
        
        return queryset.filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(user__email__icontains=value) |
            Q(student_id__icontains=value)
        )