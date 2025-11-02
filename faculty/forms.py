# --- File: faculty/forms.py ---
# This is the full and correct file (FIXED)

from django import forms
from django.db import transaction
from django.contrib.auth.hashers import make_password
from core.models import User
from .models import Faculty, Department

class FacultyForm(forms.ModelForm):
    # User fields
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)

    class Meta:
        model = Faculty
        fields = [
            'employee_id', 'designation', 'phone', 'alternate_phone', 
            'personal_email', 'address', 'qualification', 'specialization', 
            'joining_date', 'salary', 'status', 'employment_type',
        ]
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If this is an existing instance, populate the User fields
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['department'].initial = self.instance.department
            
            # Make User fields read-only during edit
            self.fields['email'].disabled = True
            self.fields['employee_id'].disabled = True # Cannot change employee ID
        
        # Apply Tailwind classes to all fields
        for field_name, field in self.fields.items():
            # Apply default classes
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-textarea'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.DateInput):
                 field.widget.attrs['class'] = 'form-input dark:[color-scheme:dark]'
            else:
                field.widget.attrs['class'] = 'form-input'
            
            # Special handling for disabled fields
            if field.disabled:
                field.widget.attrs['class'] += ' bg-muted'
                field.widget.attrs['readonly'] = True


    @transaction.atomic
    def save(self, commit=True):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        employee_id = self.cleaned_data.get('employee_id') # Changed from faculty_id
        
        if not self.instance.pk:
            # --- This is a NEW faculty ---
            try:
                # Use employee_id as default username and password
                user = User.objects.create(
                    username=employee_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    role='faculty',
                    password=make_password(employee_id)
                )
            except IntegrityError as e:
                if 'username' in str(e):
                    self.add_error('employee_id', "A user with this Employee ID already exists.")
                elif 'email' in str(e):
                    self.add_error('email', "A user with this email already exists.")
                else:
                    self.add_error(None, f"Could not create user: {e}")
                return None
            except Exception as e:
                self.add_error(None, f"Could not create user: {e}")
                return None 

            self.instance.user = user
        else:
            # --- This is an EXISTING faculty ---
            user = self.instance.user
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        faculty_profile = super().save(commit)
        
        return faculty_profile