from django import forms
from .models import Faculty
from core.models import User
from students.models import Department

class FacultyForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        """
        Filters the 'user' queryset to only show users with the 'faculty'
        role who do not already have a faculty_profile.
        """
        super().__init__(*args, **kwargs)
        
        # Per Task 1.C: Filter users
        self.fields['user'].queryset = User.objects.filter(
            role='faculty', 
            faculty_profile__isnull=True
        )
        
        # Apply Tailwind classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 rounded-md border border-input bg-background text-sm focus:ring-2 focus:ring-ring focus:border-primary transition-all'
            })

    class Meta:
        model = Faculty
        # We include all fields Admin needs to fill out
        fields = [
            'user', 
            'employee_id', 
            'department', 
            'designation', 
            'qualification',
            'experience',
            'phone', 
            'address', 
            'joining_date', 
            'salary', 
            'status'
        ]
        # Add a date picker widget for joining_date
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }
