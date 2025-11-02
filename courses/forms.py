# --- File: courses/forms.py ---
# This is the full and correct file (FIXED)

from django import forms
from .models import Course
from students.models import Department
from faculty.models import Faculty

class CourseForm(forms.ModelForm):
    # Department is still a simple selection
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)

    class Meta:
        model = Course
        # --- FIXED: Matched all fields to your courses/models.py ---
        fields = [
            'name', 'course_code', 'department', 
            'year', 'semester', 'credits', 'description', 'is_active',
            'course_type', 'lecture_hours', 'tutorial_hours', 'practical_hours',
            'syllabus', 'reference_books'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'reference_books': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Style all fields with our new Tailwind classes
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-textarea'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-checkbox h-5 w-5 rounded'
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'form-input' # Basic styling for file input
            else:
                field.widget.attrs['class'] = 'form-input'

        # --- FIXED: Removed the faculty field logic ---