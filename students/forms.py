from django import forms
from .models import Student, Department
from core.models import User
import datetime

class StudentForm(forms.ModelForm):
    # We are getting User fields to create/update the User model at the same time
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    # Make date fields use the HTML5 date picker
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    date_of_admission = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.date.today)

    class Meta:
        model = Student
        # List all fields from the Student model *and* our extra User fields
        fields = [
            'first_name', 'last_name', 'email', 'student_id', 'department', 
            'year', 'semester', 'phone', 'address', 'date_of_birth',
            'guardian_name', 'guardian_phone', 'date_of_admission', 'status'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If we are editing an existing student, populate the User fields
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            
        # Add Tailwind classes to all fields
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.DateInput):
                field.widget.attrs['class'] = 'form-input'
            else:
                # Special handling for date widgets to ensure they use the form-input class
                field.widget.attrs.update({'class': 'form-input'})

    def save(self, commit=True):
        # Save the Student instance
        student = super().save(commit=False)
        
        # Get or create the User
        try:
            user = self.instance.user
        except User.DoesNotExist:
            # Create a new user if this is a new student
            user = User(username=self.cleaned_data['student_id'])
            user.set_password(self.cleaned_data['student_id']) # Default password
            user.role = 'student'

        # Update User fields from the form
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['student_id'] # Ensure username stays synced
        
        if commit:
            user.save()
            student.user = user
            student.save()
            
        return student

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'head_of_department', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows'] = 3
        
        self.fields['head_of_department'].required = False
        self.fields['description'].required = False