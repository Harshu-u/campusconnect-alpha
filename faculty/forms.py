from django import forms
from .models import Faculty
from students.models import Department
from core.models import User

class FacultyForm(forms.ModelForm):
    # Get User fields to create/update the User model
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = Faculty
        # These fields *exactly* match our new faculty/models.py
        fields = [
            'first_name', 'last_name', 'email', 'faculty_id', 'department',
            'designation', 'specialization', 'phone', 'office_location',
            'status', 'date_of_joining'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing, populate the User fields
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

        # Add Tailwind classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'

    def save(self, commit=True):
        faculty = super().save(commit=False)
        
        # Get or create the User
        try:
            user = self.instance.user
        except User.DoesNotExist:
            # Create a new user if this is a new faculty member
            user = User(username=self.cleaned_data['faculty_id'])
            user.set_password(self.cleaned_data['faculty_id']) # Default password
            user.role = 'faculty'

        # Update User fields from the form
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['faculty_id'] # Sync username
        
        if commit:
            user.save()
            faculty.user = user
            faculty.save()
            
        return faculty