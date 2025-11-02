from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'code', 'department', 'faculty', 
            'description', 'credits', 'course_type', 'status'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Tailwind classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows'] = 3
                
        # Make description not required
        self.fields['description'].required = False
        self.fields['faculty'].required = False