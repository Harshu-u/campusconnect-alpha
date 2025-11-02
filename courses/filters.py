import django_filters
from django import forms
from .models import Course, Department
from faculty.models import Faculty
from django.db.models import Q

class CourseFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_search', 
        label="Search",
        widget=forms.TextInput(attrs={'placeholder': 'Search by Title or Code...', 'class': 'form-input'})
    )
    
    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Department"
    )

    faculty = django_filters.ModelChoiceFilter(
        queryset=Faculty.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Faculty"
    )

    course_type = django_filters.ChoiceFilter(
        choices=Course.COURSE_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Type"
    )

    class Meta:
        model = Course
        fields = ['search', 'department', 'faculty', 'course_type']

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=value) |
            Q(code__icontains=value)
        )