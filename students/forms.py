from django import forms
from .models import Student, Department
from core.models import User

class StudentForm(forms.ModelForm):
    
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
        
        # Apply Tailwind classes to all fields to match the project's style
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 rounded-md border border-input bg-background text-sm'
            })

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