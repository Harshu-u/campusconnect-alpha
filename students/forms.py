# --- File: students/forms.py ---
# This is the full and correct file.

from django import forms
from .models import Student, Department
from core.models import User

class StudentForm(forms.ModelForm):
    
    # Define common CSS classes for all form widgets
    FORM_INPUT_CLASSES = 'form-input w-full px-4 py-2 rounded-lg border border-input bg-background text-sm shadow-sm placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-primary'
    FORM_SELECT_CLASSES = 'form-select w-full px-4 py-2 rounded-lg border border-input bg-background text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-primary'
    FORM_DATE_CLASSES = 'form-date w-full px-4 py-2 rounded-lg border border-input bg-background text-sm shadow-sm placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-primary'

    def __init__(self, *args, **kwargs):
        """
        Filters the 'user' queryset to only show users with the 'student'
        role who do not already have a student_profile.
        """
        super().__init__(*args, **kwargs)
        
        # Per Task 1.B: Filter users
        self.fields['user'].queryset = User.objects.filter(
            role='student', 
            student_profile__isnull=True
        )
        
        # Apply Tailwind classes to all fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.DateInput):
                 field.widget.attrs.update({'class': self.FORM_DATE_CLASSES})
            elif isinstance(field.widget, forms.Select):
                 field.widget.attrs.update({'class': self.FORM_SELECT_CLASSES})
            else:
                 field.widget.attrs.update({'class': self.FORM_INPUT_CLASSES})

    class Meta:
        model = Student
        # We include all fields Admin needs to fill out
        fields = [
            'user', 
            'student_id', 
            'department', 
            'year', 
            'semester', 
            'enrollment_date', 
            'phone', 
            'address', 
            'guardian_name', 
            'guardian_phone', 
            'status'
        ]
        # Add a date picker widget for enrollment_date
        widgets = {
            'enrollment_date': forms.DateInput(attrs={'type': 'date'}),
        }

# --- NEW DEPARTMENT FORM ---
class DepartmentForm(forms.ModelForm):
    
    # Define common CSS classes
    FORM_INPUT_CLASSES = 'form-input w-full px-4 py-2 rounded-lg border border-input bg-background text-sm shadow-sm placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-primary'
    FORM_TEXTAREA_CLASSES = 'form-input w-full px-4 py-2 rounded-lg border border-input bg-background text-sm shadow-sm placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-primary'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply Tailwind classes to all fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                 field.widget.attrs.update({'class': self.FORM_TEXTAREA_CLASSES, 'rows': 3})
            else:
                 field.widget.attrs.update({'class': self.FORM_INPUT_CLASSES})

    class Meta:
        model = Department
        fields = ['name', 'code', 'head_of_department', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }