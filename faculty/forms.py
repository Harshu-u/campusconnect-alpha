from django import forms
from .models import Faculty
from core.models import User
from students.models import Department

class FacultyForm(forms.ModelForm):
    
    # Define common CSS classes for all form widgets
    FORM_INPUT_CLASSES = 'form-input w-full px-4 py-2 rounded-lg border border-input bg-background text-sm shadow-sm placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-primary'
    FORM_SELECT_CLASSES = 'form-select w-full px-4 py-2 rounded-lg border border-input bg-background text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-primary'
    FORM_DATE_CLASSES = 'form-date w-full px-4 py-2 rounded-lg border border-input bg-background text-sm shadow-sm placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-primary'

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
            if isinstance(field.widget, forms.DateInput):
                 field.widget.attrs.update({'class': self.FORM_DATE_CLASSES})
            elif isinstance(field.widget, forms.Select):
                 field.widget.attrs.update({'class': self.FORM_SELECT_CLASSES})
            else:
                 field.widget.attrs.update({'class': self.FORM_INPUT_CLASSES})

    class Meta:
        model = Faculty
        # We include all fields Admin needs to fill out
        fields = [
            'user',
            'employee_id',
            'department',
            'designation',
            'employment_type',
            'phone',
            'alternate_phone',
            'personal_email',
            'address',
            'city',
            'state',
            'postal_code',
            'qualification',
            'specialization',
            'research_interests',
            'total_experience',
            'industry_experience',
            'teaching_experience',
            'joining_date',
            'contract_end_date',
            'salary',
            'bank_account',
            'pan_number',
            'status',
            'is_hod'
        ]
        # Add a date picker widget for joining_date
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }